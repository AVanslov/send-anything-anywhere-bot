import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.database.models import async_main
from app.handlers import (
    start,
    sender,
    carrier,
    favorites,
    history,
    availible_routes,
    send_money,
    contact_developer,
    menu,
)

load_dotenv()

TOKEN = getenv('BOT_TOKEN')


async def main() -> None:
    await async_main()
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_routers(
        start.start_router,
        sender.sender_router,
        carrier.carrier_router,
        favorites.favorites_router,
        history.history_router,
        availible_routes.availible_routes,
        send_money.send_money_router,
        contact_developer.contact_developer_router,
        menu.menu_router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
