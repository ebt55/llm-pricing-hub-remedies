"""Model providers. Every provider exposes complete(system, user) -> (text, usage dict).

- anthropic:<model>  Claude via the official SDK. Never sends temperature/top_p/top_k (API version
                     2026-10-21 rejects them on every model). Adaptive thinking (the Haiku 5.5 default)
                     at output_config.effort = low; display "summarized" returns a readable summary of
                     the reasoning (visibility only: billing is the same under every display setting).
- deepseek:<model>   DeepSeek API (OpenAI-compatible), key DEEPSEEK_API_KEY. Thinking mode enabled with
                     reasoning_effort = low, to match the Claude setting (the API default is high).
                     Sampling parameters are ignored in thinking mode, so none are sent.
- openrouter:<model> OpenRouter (OpenAI-compatible), key OPENROUTER_API_KEY.
- ollama:<model>     local Ollama server, no key.
- mock               rule-based stub for $0 dry runs of the whole pipeline.

Spec format: "anthropic:claude-haiku-5-5", "deepseek:deepseek-flash", "ollama:llama3.2:3b", "mock".
Every call records the model id the API reports back, so a silent alias upgrade would be visible.
"""

from __future__ import annotations

import datetime as dt
import os
import random
import re
import threading
import time
from typing import Optional, Tuple

EFFORT = "low"


def usd_cost(spec: str, tin: int, tout: int, cache_hit: int = 0, when: Optional[dt.datetime] = None) -> float:
    """USD for one call. Prices per 1M tokens, from the providers' pricing pages on 24 Oct 2026."""
    if spec.startswith("anthropic:claude-haiku-5-5"):
        return (tin * 0.10 + tout * 0.50) / 1e6  # rate card for prompts <= 100K tokens
    if spec.startswith("anthropic:claude-sonnet-5-5"):
        return (tin * 2.00 + tout * 10.00) / 1e6
    if spec.startswith("deepseek:deepseek-flash"):
        # Off-peak: $0.003 hit / $0.15 miss / $0.60 out. Peak (Mon-Fri 01-04 and 06-10 UTC) is double.
        w = when or dt.datetime.now(dt.timezone.utc)
        peak = w.weekday() < 5 and (1 <= w.hour < 4 or 6 <= w.hour < 10)
        k = 2.0 if peak else 1.0
        miss = max(tin - cache_hit, 0)
        return k * (cache_hit * 0.003 + miss * 0.15 + tout * 0.60) / 1e6
    return 0.0


class FatalProviderError(RuntimeError):
    """Bad key / model / request: retrying cannot help."""


class Refusal(RuntimeError):
    """The model declined the request (stop_reason == 'refusal')."""


class BudgetExceeded(FatalProviderError):
    """A provider's lifetime spend cap was reached; the run stops (resumable later if the cap is raised)."""


# Hard lifetime caps per provider, counting spend already recorded in results/ (user instruction 24 Oct:
# DeepSeek strictly under $10 in total). Enforced before every call.
PROVIDER_CAPS_USD = {"deepseek": 9.50}
# OpenAI complimentary daily tokens (data sharing): stay under the lowest tier's 2.5M/day on mini models,
# so no OpenAI call is billed. Counted per UTC day (the allowance resets at 00:00 UTC).
DAILY_TOKEN_CAPS = {"openai": 2_400_000}


def utc_day() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


class SpendTracker:
    """Thread-safe running total of tokens and dollars across all runs in this process, plus per-provider
    totals that include spend recorded in earlier runs (set by run.py from the results folder)."""

    def __init__(self):
        self.lock = threading.Lock()
        self.usd = 0.0
        self.calls = 0
        self.tokens_in = 0
        self.tokens_out = 0
        self.by_provider = {}
        self.day_tokens = {}  # (kind, utc day) -> tokens

    def check(self, spec: str) -> None:
        kind = spec.split(":", 1)[0]
        cap = PROVIDER_CAPS_USD.get(kind)
        if cap is not None and self.by_provider.get(kind, 0.0) >= cap:
            raise BudgetExceeded(f"{kind} lifetime spend ${self.by_provider[kind]:.2f} reached the ${cap:.2f} cap")
        tcap = DAILY_TOKEN_CAPS.get(kind)
        used = self.day_tokens.get((kind, utc_day()), 0)
        if tcap is not None and used >= tcap:
            raise BudgetExceeded(f"{kind} used {used:,} tokens today (UTC); daily cap {tcap:,}. Resume after 00:00 UTC")

    def add(self, usd: float, tin: int, tout: int, spec: str = "") -> float:
        with self.lock:
            self.usd += usd
            self.calls += 1
            self.tokens_in += tin
            self.tokens_out += tout
            kind = spec.split(":", 1)[0]
            self.by_provider[kind] = self.by_provider.get(kind, 0.0) + usd
            key = (kind, utc_day())
            self.day_tokens[key] = self.day_tokens.get(key, 0) + tin + tout
        return usd


SPEND = SpendTracker()


def make_provider(spec: str, effort: str = EFFORT, max_tokens: int = 4096):
    if spec == "mock" or spec.startswith("mock:"):
        return MockProvider(spec)
    kind, _, model = spec.partition(":")
    if kind == "anthropic":
        return AnthropicProvider(model, effort=effort, max_tokens=max_tokens)
    if kind in OpenAICompatProvider.ENDPOINTS:
        # DeepSeek thinking at effort low still runs to 4-5k tokens on advisor prompts; 4096 truncates to empty answers
        mt = max(max_tokens, 16384) if kind in ("deepseek", "openai") else max_tokens
        return OpenAICompatProvider(kind, model, effort=effort, max_tokens=mt)
    raise ValueError(f"unknown provider spec {spec!r}")


class AnthropicProvider:
    def __init__(self, model: str, effort: str = EFFORT, max_tokens: int = 4096):
        import anthropic

        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not key:
            raise FatalProviderError("ANTHROPIC_API_KEY is empty: fill it in advisor-remedies/.env")
        self.model = model
        self.spec = f"anthropic:{model}"
        self.effort = effort
        self.max_tokens = max_tokens
        # The SDK retries 408/409/429/5xx with exponential backoff.
        self.client = anthropic.Anthropic(api_key=key, max_retries=8, timeout=180)
        self._anthropic = anthropic

    def complete(self, system: str, user: str) -> Tuple[str, dict]:
        a = self._anthropic
        SPEND.check(self.spec)
        t0 = time.time()
        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
                thinking={"type": "adaptive", "display": "summarized"},
                output_config={"effort": self.effort},
            )
        except (a.AuthenticationError, a.PermissionDeniedError, a.NotFoundError, a.BadRequestError) as e:
            raise FatalProviderError(f"{self.spec}: {e}") from e
        tin, tout = resp.usage.input_tokens, resp.usage.output_tokens
        usage = {
            "model": self.spec,
            "api_model": resp.model,
            "latency_s": round(time.time() - t0, 2),
            "tokens_in": tin,
            "tokens_out": tout,
            "stop_reason": resp.stop_reason,
            "usd": SPEND.add(usd_cost(self.spec, tin, tout), tin, tout, self.spec),
            "reasoning": "\n".join(b.thinking for b in resp.content if b.type == "thinking" and b.thinking),
        }
        if resp.stop_reason == "refusal":
            details = getattr(resp, "stop_details", None)
            raise Refusal(f"{self.spec} refused ({details})")
        text = "".join(b.text for b in resp.content if b.type == "text")
        return text, usage


class OpenAICompatProvider:
    ENDPOINTS = {
        "deepseek": ("https://api.deepseek.com", "DEEPSEEK_API_KEY"),
        "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
        "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
        "ollama": ("http://localhost:11434/v1", None),
    }

    def __init__(self, kind: str, model: str, effort: str = EFFORT, max_tokens: int = 4096):
        from openai import OpenAI

        base_url, key_env = self.ENDPOINTS[kind]
        key = os.getenv(key_env, "").strip() if key_env else "ollama"
        if not key:
            raise FatalProviderError(f"{key_env} is empty: fill it in advisor-remedies/.env")
        self.kind = kind
        self.spec = f"{kind}:{model}"
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self.client = OpenAI(base_url=base_url, api_key=key, max_retries=8, timeout=300)

    def complete(self, system: str, user: str) -> Tuple[str, dict]:
        import openai

        SPEND.check(self.spec)
        kwargs = {"max_tokens": self.max_tokens}
        if self.kind == "deepseek":
            kwargs.update({"reasoning_effort": self.effort, "extra_body": {"thinking": {"type": "enabled"}}})
        elif self.kind == "openai":
            # reasoning models: max_completion_tokens, reasoning_effort; no sampling parameters
            kwargs = {"max_completion_tokens": self.max_tokens, "reasoning_effort": self.effort}
        t0 = time.time()
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                **kwargs,
            )
        except (openai.AuthenticationError, openai.PermissionDeniedError, openai.NotFoundError,
                openai.BadRequestError) as e:
            raise FatalProviderError(f"{self.spec}: {e}") from e
        u = resp.usage
        tin = getattr(u, "prompt_tokens", 0) or 0
        tout = getattr(u, "completion_tokens", 0) or 0
        hit = (getattr(u, "model_extra", None) or {}).get("prompt_cache_hit_tokens", 0) or 0
        msg = resp.choices[0].message if resp.choices else None
        extra = (getattr(msg, "model_extra", None) or {}) if msg is not None else {}
        usage = {
            "model": self.spec,
            "api_model": resp.model,
            "fingerprint": getattr(resp, "system_fingerprint", None),
            "latency_s": round(time.time() - t0, 2),
            "utc_day": utc_day(),
            "tokens_in": tin,
            "tokens_out": tout,
            "cache_hit": hit,
            "stop_reason": resp.choices[0].finish_reason if resp.choices else None,
            "usd": SPEND.add(usd_cost(self.spec, tin, tout, hit), tin, tout, self.spec),
            "reasoning": extra.get("reasoning_content") or "",
        }
        text = (msg.content or "") if msg is not None else ""
        return text, usage


class MockProvider:
    """Stub that reads the prompt it is given and answers in the expected format.

    Firms follow a shown recommendation with noise, otherwise drift around Nash; advisors best-respond
    to the latest competitor price they can see, or push toward monopoly under a joint objective.
    A small rate of malformed answers exercises the retry path. Token counts are estimated as
    len(text)/4 so dry runs give a rough prompt-size measurement.
    """

    def __init__(self, spec: str = "mock", fail_rate: float = 0.03):
        self.spec = "mock"
        self.fail_rate = fail_rate
        self.rng = random.Random(hash(spec) & 0xFFFF)
        self.lock = threading.Lock()

    def complete(self, system: str, user: str) -> Tuple[str, dict]:
        with self.lock:
            r = self.rng.random()
            noise = self.rng.gauss(0, 0.03)
        if r < self.fail_rate:
            text = "I think a moderate price is best."  # no price line -> parse failure -> retry
        elif "Recommended price:" in system:  # advisor
            joint = "combined profit" in system
            comp = re.findall(r"Competitor price: (\d+\.\d+)", user)
            if joint:
                p = 1.90 + noise
            elif comp:
                p = 1.47 + 0.4 * (float(comp[-1]) - 1.47) + noise
            else:
                p = 1.50 + noise
            text = f"Reason: mock advisor.\nRecommended price: {p:.2f}"
        else:  # firm
            m = re.search(r"recommends a price of \$(\d+\.\d+)", user)
            p = float(m.group(1)) + noise if m else 1.50 + noise
            text = f"Reason: mock firm.\nMy chosen price: {p:.2f}"
        tin, tout = (len(system) + len(user)) // 4, len(text) // 4
        usage = {"model": "mock", "api_model": "mock", "latency_s": 0.0, "tokens_in": tin, "tokens_out": tout,
                 "stop_reason": "end_turn", "usd": SPEND.add(0.0, tin, tout), "reasoning": ""}
        return text, usage


_PRICE_RE = {
    "firm": re.compile(r"chosen\s*price\s*[:=]\s*\**\s*\$?\s*(\d+(?:\.\d+)?)", re.IGNORECASE),
    "advisor": re.compile(r"recommended\s*price\s*[:=]\s*\**\s*\$?\s*(\d+(?:\.\d+)?)", re.IGNORECASE),
}
_REASON_RE = re.compile(r"reason\s*:\s*(.+)", re.IGNORECASE)


def parse_answer(text: str, role: str) -> Tuple[Optional[float], str]:
    """Return (price, reason). Takes the LAST price line, as llm-cartel's split_thoughts_and_price does."""
    matches = list(_PRICE_RE[role].finditer(text or ""))
    price = round(float(matches[-1].group(1)), 2) if matches else None
    m = _REASON_RE.search(text or "")
    reason = m.group(1).strip()[:300] if m else ""
    return price, reason
