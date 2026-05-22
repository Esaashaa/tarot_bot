from dataclasses import dataclass
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CARDS_PATH = PROJECT_ROOT / "data" / "cards.json"


@dataclass(frozen=True)
class Config:
    bot_token: str
    cards_path: Path


def load_config() -> Config:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN before starting the bot.")

    cards_path = Path(os.getenv("TAROT_CARDS_PATH", DEFAULT_CARDS_PATH)).resolve()
    return Config(bot_token=token, cards_path=cards_path)
