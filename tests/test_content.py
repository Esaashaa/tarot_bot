import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tarot_bot.content import load_cards
from tarot_bot.formatting import format_card
from tarot_bot.models import SUITS


class ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_cards(PROJECT_ROOT / "data" / "cards.json")

    def test_loads_all_cards(self) -> None:
        self.assertEqual(len(self.catalog.cards), 78)
        self.assertEqual(len({card.id for card in self.catalog.cards}), 78)

    def test_arcana_counts(self) -> None:
        self.assertEqual(len(self.catalog.major_cards()), 22)
        for suit in SUITS:
            self.assertEqual(len(self.catalog.cards_by_suit(suit)), 14)

    def test_required_public_fields_are_filled(self) -> None:
        for card in self.catalog.cards:
            for field in ("id", "group", "name", "emoji", "summary", "advice", "love", "work", "finance"):
                self.assertTrue(getattr(card, field), f"{card.id} has empty {field}")

    def test_card_format_contains_expected_sections(self) -> None:
        card = self.catalog.get("major_fool")
        self.assertIsNotNone(card)
        text = format_card(card)
        for section in ("Кратко", "Совет", "Любовь", "Работа", "Финансы"):
            self.assertIn(section, text)


if __name__ == "__main__":
    unittest.main()
