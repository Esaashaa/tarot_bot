import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from tarot_bot.content import CardCatalog
from tarot_bot.formatting import format_card
from tarot_bot.models import SUIT_TITLES
from tarot_bot.navigation import (
    CB_GUIDE,
    CB_MAIN,
    CB_MAJOR,
    CB_MINOR,
    card_actions,
    error_menu,
    guide_menu,
    main_menu,
    major_cards_menu,
    minor_cards_menu,
    suits_menu,
)


logger = logging.getLogger(__name__)
router = Router()


WELCOME_TEXT = (
    "Привет! Я помогу быстро найти значение карты Таро.\n\n"
    "Выбери раздел ниже, а дальше просто нажимай кнопки."
)

GUIDE_TEXT = "Выбери раздел справочника:"
TEXT_FALLBACK = "Я пока понимаю только кнопки. Открой справочник через меню ниже."


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu())


@router.callback_query(F.data == CB_MAIN)
async def show_main_menu(callback: CallbackQuery) -> None:
    await _edit(callback, WELCOME_TEXT, main_menu())


@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery) -> None:
    await _edit(
        callback,
        "Это справочник Таро для начинающих: выбери карту и получи короткое толкование.",
        main_menu(),
    )


@router.callback_query(F.data == CB_GUIDE)
async def show_guide(callback: CallbackQuery) -> None:
    await _edit(callback, GUIDE_TEXT, guide_menu())


@router.callback_query(F.data == CB_MAJOR)
async def show_major_cards(callback: CallbackQuery, catalog: CardCatalog) -> None:
    await _edit(callback, "Старшие арканы:", major_cards_menu(catalog))


@router.callback_query(F.data == CB_MINOR)
async def show_suits(callback: CallbackQuery) -> None:
    await _edit(callback, "Выбери масть младших арканов:", suits_menu())


@router.callback_query(F.data.startswith("suit:"))
async def show_minor_cards(callback: CallbackQuery, catalog: CardCatalog) -> None:
    suit = (callback.data or "").split(":", 1)[1]
    title = SUIT_TITLES.get(suit)
    if title is None:
        await _show_not_found(callback)
        return

    await _edit(callback, f"{title}: выбери карту", minor_cards_menu(catalog, suit))


@router.callback_query(F.data.startswith("card:"))
async def show_card(callback: CallbackQuery, catalog: CardCatalog) -> None:
    card_id = (callback.data or "").split(":", 1)[1]
    card = catalog.get(card_id)
    if card is None:
        logger.warning("Unknown card requested: %s", card_id)
        await _show_not_found(callback)
        return

    await _edit(callback, format_card(card), card_actions(card))


@router.message()
async def handle_text_fallback(message: Message) -> None:
    await message.answer(TEXT_FALLBACK, reply_markup=main_menu())


async def _show_not_found(callback: CallbackQuery) -> None:
    await _edit(callback, "Не удалось найти карту. Вернись в главное меню и попробуй снова.", error_menu())


async def _edit(callback: CallbackQuery, text: str, reply_markup) -> None:
    if callback.message is None:
        await callback.answer("Сообщение устарело. Открой меню заново.", show_alert=True)
        return

    await callback.message.edit_text(text, reply_markup=reply_markup)
    await callback.answer()
