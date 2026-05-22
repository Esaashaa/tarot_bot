from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tarot_bot.content import CardCatalog
from tarot_bot.models import SUITS, SUIT_TITLES, Card


CB_MAIN = "menu:main"
CB_GUIDE = "guide:root"
CB_MAJOR = "guide:major"
CB_MINOR = "guide:minor"


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Справочник карт", callback_data=CB_GUIDE)],
            [InlineKeyboardButton(text="О боте", callback_data="about")],
        ]
    )


def guide_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌟 Старшие арканы", callback_data=CB_MAJOR)],
            [InlineKeyboardButton(text="🪄 Младшие арканы", callback_data=CB_MINOR)],
            [InlineKeyboardButton(text="В главное меню", callback_data=CB_MAIN)],
        ]
    )


def major_cards_menu(catalog: CardCatalog) -> InlineKeyboardMarkup:
    rows = [[_card_button(card)] for card in catalog.major_cards()]
    rows.append([InlineKeyboardButton(text="Назад", callback_data=CB_GUIDE)])
    rows.append([InlineKeyboardButton(text="В главное меню", callback_data=CB_MAIN)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def suits_menu() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=SUIT_TITLES[suit], callback_data=f"suit:{suit}")]
        for suit in SUITS
    ]
    rows.append([InlineKeyboardButton(text="Назад", callback_data=CB_GUIDE)])
    rows.append([InlineKeyboardButton(text="В главное меню", callback_data=CB_MAIN)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def minor_cards_menu(catalog: CardCatalog, suit: str) -> InlineKeyboardMarkup:
    rows = [[_card_button(card)] for card in catalog.cards_by_suit(suit)]
    rows.append([InlineKeyboardButton(text="Назад", callback_data=CB_MINOR)])
    rows.append([InlineKeyboardButton(text="В главное меню", callback_data=CB_MAIN)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def card_actions(card: Card) -> InlineKeyboardMarkup:
    back_callback = CB_MAJOR if card.suit is None else f"suit:{card.suit}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад к списку", callback_data=back_callback)],
            [InlineKeyboardButton(text="В главное меню", callback_data=CB_MAIN)],
        ]
    )


def error_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В главное меню", callback_data=CB_MAIN)],
        ]
    )


def _card_button(card: Card) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=f"{card.emoji} {card.name}", callback_data=f"card:{card.id}")
