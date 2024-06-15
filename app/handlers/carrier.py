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
from app.states import CarrierData

carrier_router = Router()


@carrier_router.callback_query(F.data == 'want_to_delivery')
async def carrier_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'want_to_delivery'
    and starts the procedure for creating
    an announcement about
    the ability to deliver a package.
    """
    await callback.answer(
        'Ура! Вы всего в паре шагов от доаставки подходящей посылки.'
    )
    await callback.message.delete()
    await state.set_state(CarrierData.date_of_the_trip)
    await callback.message.answer(
        'Выберите дату вашей поездки',
        reply_markup=await kb.years_calendar_keyboard()
    )
