import json
from pathlib import Path
from typing import Any

from tarot_bot.models import GROUP_MAJOR, GROUP_MINOR, SUITS, Card


REQUIRED_FIELDS = (
    "id",
    "group",
    "name",
    "emoji",
    "summary",
    "advice",
    "love",
    "work",
    "finance",
)


class ContentError(ValueError):
    """Raised when card content is missing or invalid."""


class CardCatalog:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self._by_id = {card.id: card for card in cards}
        if len(self._by_id) != len(cards):
            raise ContentError("Card ids must be unique.")
        self._validate_catalog()

    def major_cards(self) -> list[Card]:
        return [card for card in self.cards if card.group == GROUP_MAJOR]

    def minor_cards(self) -> list[Card]:
        return [card for card in self.cards if card.group == GROUP_MINOR]

    def cards_by_suit(self, suit: str) -> list[Card]:
        return [card for card in self.cards if card.suit == suit]

    def get(self, card_id: str) -> Card | None:
        return self._by_id.get(card_id)

    def _validate_catalog(self) -> None:
        if len(self.cards) != 78:
            raise ContentError(f"Expected 78 cards, got {len(self.cards)}.")
        if len(self.major_cards()) != 22:
            raise ContentError("Expected 22 major arcana cards.")
        for suit in SUITS:
            if len(self.cards_by_suit(suit)) != 14:
                raise ContentError(f"Expected 14 cards for suit '{suit}'.")


def load_cards(path: Path) -> CardCatalog:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ContentError(f"Cannot read cards file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContentError(f"Cards file is not valid JSON: {path}") from exc

    raw_cards = payload.get("cards") if isinstance(payload, dict) else payload
    if not isinstance(raw_cards, list):
        raise ContentError("Cards file must contain a list or an object with a 'cards' list.")

    return CardCatalog([_parse_card(raw_card) for raw_card in raw_cards])


def _parse_card(raw: Any) -> Card:
    if not isinstance(raw, dict):
        raise ContentError("Every card must be an object.")

    missing_fields = [field for field in REQUIRED_FIELDS if not raw.get(field)]
    if missing_fields:
        card_id = raw.get("id", "<unknown>")
        raise ContentError(f"Card {card_id} is missing required fields: {missing_fields}.")

    group = raw["group"]
    suit = raw.get("suit")
    if group == GROUP_MAJOR and suit is not None:
        raise ContentError(f"Major arcana card {raw['id']} must not have a suit.")
    if group == GROUP_MINOR and suit not in SUITS:
        raise ContentError(f"Minor arcana card {raw['id']} has invalid suit: {suit}.")
    if group not in (GROUP_MAJOR, GROUP_MINOR):
        raise ContentError(f"Card {raw['id']} has invalid group: {group}.")

    return Card(
        id=raw["id"],
        group=group,
        suit=suit,
        name=raw["name"],
        emoji=raw["emoji"],
        summary=raw["summary"],
        advice=raw["advice"],
        love=raw["love"],
        work=raw["work"],
        finance=raw["finance"],
        reversed=raw.get("reversed"),
        image_path=raw.get("image_path"),
    )
