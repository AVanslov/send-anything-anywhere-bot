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

favorites_router = Router()


@favorites_router.callback_query(F.data == 'favorite')
async def carrier_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'favorite'
    and starts the procedure for creating
    an announcement about
    the ability to deliver a package.
    """
    await callback.answer(
        'Давайте посмотрим, что там у нас в избранном.'
    )
    await callback.message.delete()
    await callback.message.answer(
        'Избранное',  # GET запрос в БД на список объектов
        # reply_markup=await kb.years_calendar_keyboard()
    )
