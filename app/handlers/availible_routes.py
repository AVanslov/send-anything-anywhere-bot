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
import app.database.requests as rq
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
    # await callback.message.answer(
    #     'Доступные направления\n'
    #     'Формируем картинку с картой и стрелочками',
    #     reply_markup=await kb.make_inline_keyboard(['menu'], 1)
    # )
    carrier_adds = await rq.get_carrier_add_items()
    if carrier_adds:
        for add in carrier_adds:
            await callback.message.answer(
                'Рейтинг: ⭐⭐⭐⭐⭐\n'
                'Отзывов : 10\n'
                'Выполнено доставок : 10\n'
                'Маршрут: {departure_city}\n'
                'Дата отправления: {delivery_date}\n'
                'Дата прибытия в {arrival_city}: \n'
                'Допустимые габариты посылки: {size}\n'
                'Допустимая масса посылки: {weight}\n'
                'Желаемое вознаграждение: {type_of_reward}\n'
                'Допустимое содержимое посылки: {cargo_type}\n'
                'Вид транспорта: {transport}\n'.format(
                    departure_city=add.departure_city,
                    arrival_city=add.arrival_city,
                    delivery_date=add.delivery_date,
                    size=add.size,
                    weight=add.weight,
                    type_of_reward=add.type_of_reward,
                    cargo_type=add.cargo_type,
                    transport=add.transport
                ),
                reply_markup=await kb.make_inline_keyboard(
                    ['Добавить в избранное', 'Отправить посылку'], 1
                )
            )
    else:
        await callback.message.answer(
            'Cписок подходящих объявлений.\n'
            'Подходящие объявления не найдены,'
            'Нажмите кнопку ниже "Подписаться"'
            'и мы пришлем вам релевантные объявления, как только они появятся',
        )

# пишем функцию, которая
# получает все пары страна + город отправления + прибытия
# подключаем бибилиотеку Plotly и строим диаграму с картой и стрелочками
# сохраняем диаграму в файл
