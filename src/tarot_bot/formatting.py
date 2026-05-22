from html import escape

from tarot_bot.models import Card


def format_card(card: Card) -> str:
    return "\n\n".join(
        [
            f"{escape(card.emoji)} <b>{escape(card.name)}</b>",
            _section("Кратко", card.summary),
            _section("Совет", card.advice),
            _section("Любовь", card.love),
            _section("Работа", card.work),
            _section("Финансы", card.finance),
        ]
    )


def _section(title: str, text: str) -> str:
    return f"<b>{escape(title)}:</b> {escape(text)}"
