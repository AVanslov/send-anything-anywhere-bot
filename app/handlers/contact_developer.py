from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.constants import (
    ALPHABET_EN,
    CARGO_TIPES,
    CURRENCIES,
    IGNORE,
    SIZE,
    TRANSPORT,
)
import app.keyboards as kb

contact_developer_router = Router()


@contact_developer_router.callback_query(F.data == 'contact_developer')
async def contact_developer_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'contact_developer'
    and starts the procedure of creating message for developer.
    """
    await callback.answer(
        'Здесь вы можете предлжить улучшение,'
        'написать об ошибках или предложить сотрудничество разработчику.'
    )
    await callback.message.delete()
    await callback.message.answer(
        'Написать разработчику',
        reply_markup=await kb.make_inline_keyboard(['menu'], 1)
    )

# напишем функцию, которая из бота отправит сообщение
# с информацией об отправителе админу
