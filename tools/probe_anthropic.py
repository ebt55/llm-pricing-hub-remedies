"""Exit 0 if a minimal Haiku call succeeds (the workspace limit is lifted), 1 otherwise. Costs ~$0.0001."""
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"), override=True)
try:
    anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]).messages.create(
        model="claude-haiku-5-5", max_tokens=16, thinking={"type": "disabled"}, output_config={"effort": "low"},
        messages=[{"role": "user", "content": "Reply OK."}])
    sys.exit(0)
except Exception as e:  # noqa: BLE001
    print(str(e)[:160])
    sys.exit(1)
