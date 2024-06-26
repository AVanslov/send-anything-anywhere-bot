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

history_router = Router()


@history_router.callback_query(F.data == 'see_orders_history')
async def carrier_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'see_orders_history'
    and starts the procedure for creating
    an announcement about
    the ability to deliver a package.
    """
    await callback.answer(
        'Давайте посмотрим, что мы доставляли и отправляли.'
    )
    await callback.message.delete()
    # GET запрос на все объявления данного пользователя
    # все доставленные имеют статут архив,
    # прочие - активные - у активных есть кнопки удалить / редактировать,
    # у архивных: посмотреть планируемые поездки перевозчика/
    # написать коментарий (если человек не оставлял коментарий)
    await callback.message.answer(
        'История отправленных и доставленных посылок',
        reply_markup=await kb.make_inline_keyboard(['menu'], 1)
    )
