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

availible_routes = Router()


@availible_routes.callback_query(F.data == 'see_availible_routes')
async def carrier_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'see_availible_routes'
    and show availible routes.
    """
    await callback.answer(
        'Давайте посмотрим маршруты наших посылок.'
    )
    await callback.message.delete()
    await callback.message.answer(
        'Доступные направления\n'
        'Формируем картинку с картой и стрелочками',
        reply_markup=await kb.make_inline_keyboard(['menu'], 1)
    )

# пишем функцию, которая
# получает все пары страна + город отправления + прибытия
# подключаем бибилиотеку Plotly и строим диаграму с картой и стрелочками
# сохраняем диаграму в файл
