from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.database.requests as rq
import app.keyboards as kb

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await rq.set_user(message.from_user.id)
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=await kb.main_menu()
    )
