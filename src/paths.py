from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_DIR = ROOT / "bank"
SESSIONS_DIR = ROOT / "sessions"

SESSIONS_DIR.mkdir(exist_ok=True)