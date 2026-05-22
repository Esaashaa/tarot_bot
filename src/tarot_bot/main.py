import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from tarot_bot.config import load_config
from tarot_bot.content import ContentError, load_cards
from tarot_bot.handlers import router


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = load_config()
    try:
        catalog = load_cards(config.cards_path)
    except ContentError:
        logging.exception("Cannot start bot because card content is invalid.")
        raise

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot, catalog=catalog)


if __name__ == "__main__":
    asyncio.run(main())
