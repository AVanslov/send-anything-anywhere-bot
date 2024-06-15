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

send_money_router = Router()


@send_money_router.callback_query(F.data == 'send_money')
async def contact_developer_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'send_money'
    and starts the procedure of send money.
    """
    await callback.answer(
        'Здесь вы можете поблагодарить разработчика за создание сервиса.'
    )
    await callback.message.delete()
    await callback.message.answer(
        'Написать разработчику',
        # reply_markup=await kb.years_calendar_keyboard()
    )
