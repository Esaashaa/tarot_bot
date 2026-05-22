from dataclasses import dataclass


GROUP_MAJOR = "major"
GROUP_MINOR = "minor"

SUITS = ("wands", "cups", "swords", "pentacles")
SUIT_TITLES = {
    "wands": "🔥 Жезлы",
    "cups": "💧 Кубки",
    "swords": "🗡️ Мечи",
    "pentacles": "🪙 Пентакли",
}


@dataclass(frozen=True)
class Card:
    id: str
    group: str
    suit: str | None
    name: str
    emoji: str
    summary: str
    advice: str
    love: str
    work: str
    finance: str
    reversed: dict | None = None
    image_path: str | None = None
