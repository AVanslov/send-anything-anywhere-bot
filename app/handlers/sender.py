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
from app.states import SendersData

sender_router = Router()


@sender_router.callback_query(F.data == 'want_to_send')
async def send_parcel_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive calback data 'want_to_send'
    and starts the procedure for creating
    an announcement about the need to send a parcel.
    """
    await callback.answer('Давайте скорее найдем перевозчика для вашего груза')
    await callback.message.delete()
    await state.set_state(SendersData.delivery_date_year)
    await callback.message.answer(
        'Выберите желаемую дату доставки',
        reply_markup=await kb.years_calendar_keyboard()
    )


@sender_router.callback_query(SendersData.delivery_date_year)
async def senders_data_delivery_date_year(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Show Inline buttons with months.
    """
    await state.update_data(delivery_date_year=callback.data)
    await callback.message.delete()
    await callback.answer('Выберите месяц')
    await state.set_state(SendersData.delivery_date_month)
    data = await state.get_data()
    await callback.message.answer(
        (
            'Выберите желаемую дату доставки\nВы выбрали:\nГод - {year}'
        ).format(
            year=data['delivery_date_year'],
        ),
        reply_markup=await kb.months_calendar_keyboard()
    )


@sender_router.callback_query(SendersData.delivery_date_month)
async def senders_data_delivery_date_month(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Show Inline buttons of days for selected year and month.
    """
    await state.update_data(delivery_date_month=callback.data)
    await callback.message.delete()
    await callback.answer('Выберите день')
    await state.set_state(SendersData.delivery_date)
    data = await state.get_data()
    await callback.message.answer(
        (
            'Выберите желаемую дату доставки\nВы выбрали:\n'
            'Год - {year}, месяц - {month}'
        ).format(
            year=data['delivery_date_year'],
            month=data['delivery_date_month']
        ),
        reply_markup=await kb.calendar_keyboard(
            date=datetime(
                int(data['delivery_date_year']),
                int(data['delivery_date_month']),
                1
            )
        )
    )


@sender_router.callback_query(SendersData.delivery_date, F.data != IGNORE)
async def senders_data_delivery_date(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with delivery date
    save delivery date to data
    and send a request for departure cauntry.
    """
    data = await state.get_data()
    await state.update_data(
        delivery_date=datetime(
            int(data['delivery_date_year']),
            int(data['delivery_date_month']),
            int(callback.data)
        )
    )
    await callback.message.delete()
    await callback.answer('Выберите первую букву из названия страны')
    await state.set_state(SendersData.departure_country_letter)
    await callback.message.answer(
        'Укажите страну отправления',
        # добавляем inline клавиатуру для выбора первой
        # буквы из названия страны
        reply_markup=await kb.make_inline_keyboard(ALPHABET_EN, 4)
    )


@sender_router.callback_query(SendersData.departure_country_letter)
async def senders_data_departure_country_letter(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with first letter of
    departure country
    show buttons with countries
    save departure country to data
    and send a request for departure_city.
    """
    await state.update_data(departure_country_letter=callback.data)
    await callback.message.delete()
    await callback.answer('Выберите страну')
    await state.set_state(SendersData.departure_country)
    data = await state.get_data()
    await callback.message.answer(
        'Укажите страну отправления',
        reply_markup=await kb.countries(data['departure_country_letter'])
    )


@sender_router.callback_query(SendersData.departure_country)
async def senders_data_departure_country(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with name of
    departure country
    show buttons with cities of this country,
    save departure country to data
    and send a request for departure_city.
    """
    await state.update_data(departure_country=callback.data)
    await callback.message.delete()
    await callback.answer('Выберите город')
    await state.set_state(SendersData.departure_city)
    data = await state.get_data()
    await callback.message.answer(
        'Укажите город отправления',
        reply_markup=await kb.cities(data['departure_country'])
    )


@sender_router.callback_query(SendersData.departure_city)
async def senders_data_departure_city(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with departure_city
    save departure_city to data
    and send a request for departure_details.
    """
    await state.update_data(departure_city=callback.data)
    await callback.message.delete()
    await callback.answer('Укажите дополнительную информацию об отправке.')
    await state.set_state(SendersData.departure_details)
    await callback.message.answer(
        'Дополнительная информация, например,'
        'где нужно забрать посылку - вы сами привезете её к перевозчику,'
        'в аэропорт или перевозчик должен заехать к вам и тд. и т.п.'
    )


@sender_router.message(SendersData.departure_details)
async def senders_data_departure_details(
    message: Message, state: FSMContext
) -> None:
    """
    This handler recive a message with departure_city
    save departure_city to data
    and send a request for arrival_country.
    """
    await state.update_data(departure_details=message.text)
    await state.set_state(SendersData.arrival_country_letter)
    await message.answer(
        'Укажите страну прибытия',
        reply_markup=await kb.make_inline_keyboard(ALPHABET_EN, 4)
    )


@sender_router.callback_query(SendersData.arrival_country_letter)
async def senders_data_arrival_country_letter(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with arrival_country
    save arrival_country to data
    and send a request for type_of_reward.
    """
    await state.update_data(arrival_country_letter=callback.data)
    await callback.message.delete()
    await state.set_state(SendersData.arrival_country)
    data = await state.get_data()
    await callback.message.answer(
        'Укажите страну прибытия',
        reply_markup=await kb.countries(data['arrival_country_letter'])
    )


@sender_router.callback_query(SendersData.arrival_country)
async def senders_data_arrival_country(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with arrival_country
    save arrival_country to data
    and send a request for arrival_city.
    """
    await state.update_data(arrival_country=callback.data)
    await callback.message.delete()
    await state.set_state(SendersData.arrival_city)
    data = await state.get_data()
    # оценка количества городов
    # если городов более 20,
    # показываем алфавитную клавиатуру для выбора города / пагинацию
    await callback.message.answer(
        'Укажите город прибытия',
        reply_markup=await kb.cities(data['arrival_country'])
    )


@sender_router.callback_query(SendersData.arrival_city)
async def senders_data_arrival_city(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with arrival_city
    save arrival_city to data
    and send a request for type_of_reward.
    """
    await state.update_data(arrival_city=callback.data)
    await callback.message.delete()
    await callback.answer('Укажите дополнительную информацию о вручении.')
    await state.set_state(SendersData.arrival_details)
    await callback.message.answer(
        'Дополнительная информация, например,'
        'eсть ли доп. требования: отправить по почте,'
        'передать в аэропорту и тд. и тп.'
    )


@sender_router.message(SendersData.arrival_details)
async def senders_data_arrival_details(
    message: Message, state: FSMContext
) -> None:
    """
    This handler recive a message with arrival_details
    save arrival_details to data
    and send a request for type_of_reward.
    """
    await state.update_data(arrival_details=message.text)
    await state.set_state(SendersData.type_of_reward)
    await message.answer(
        'Укажите тип вознаграждения',
        reply_markup=await kb.type_of_reward()
    )


@sender_router.callback_query(SendersData.type_of_reward, F.data == 'money')
async def senders_data_type_of_reward(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward
    save type_of_reward to data
    and send a currency selection request.
    """
    await state.update_data(type_of_reward=callback.data)
    await callback.message.delete()
    await callback.answer('Выбор валюты')
    await state.set_state(SendersData.type_of_reward_currency)
    await callback.message.answer(
        'Выберите валюту',
        reply_markup=await kb.make_inline_keyboard(CURRENCIES, 2)
    )


@sender_router.callback_query(SendersData.type_of_reward_currency)
async def senders_data_type_of_reward_currency(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward_currency
    save type_of_reward_currency to data
    and send a request for type_of_reward_value.
    """
    await state.update_data(type_of_reward_currency=callback.data)
    await callback.message.delete()
    await callback.answer('Выбор суммы')
    await state.set_state(SendersData.type_of_reward_value)
    await callback.message.answer('Укажите сумму вознаграждения')


@sender_router.callback_query(SendersData.type_of_reward, F.data == 'other')
async def senders_data_type_of_reward_other(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward
    save type_of_reward to data
    and send a currency selection request.
    """
    await state.update_data(type_of_reward=callback.data)
    await callback.message.delete()
    await callback.answer('Ввод комментария')
    await state.set_state(SendersData.type_of_reward_message)
    await callback.message.answer(
        'Укажите комментарий к вознагрождению, например:'
        '"по договорённости",'
        '"за коробку конфет",'
        '"бесплатно"'
        'и ид. и т.п.'
    )


@sender_router.message(SendersData.type_of_reward_message)
async def senders_data_type_of_reward_message(
    message: Message, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward_message
    save type_of_reward_message to data
    and send a request for size.
    """
    await state.update_data(type_of_reward_message=message.text)
    await state.set_state(SendersData.size)
    await message.answer(
        'Укажите габариты посылки',
        reply_markup=await kb.make_inline_keyboard(SIZE, 1)
    )


@sender_router.message(SendersData.type_of_reward_value)
async def senders_data_type_of_reward_value(
    message: Message, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward_value
    save type_of_reward_value to data
    and send a request for size.
    """
    await state.update_data(type_of_reward_value=message.text)
    await state.set_state(SendersData.size)
    await message.answer(
        'Укажите габариты посылки',
        reply_markup=await kb.make_inline_keyboard(SIZE, 1)
    )


@sender_router.callback_query(SendersData.size)
async def senders_data_size(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with size
    save size to data
    and send a request for weight.
    """
    await state.update_data(size=callback.data)
    await callback.message.delete()
    await callback.answer('Ввод массы')
    await state.set_state(SendersData.weight)
    await callback.message.answer('Укажите массу посылки в кг.')


@sender_router.message(SendersData.weight)
async def senders_data_weight(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with weight
    save weight to data
    and send a request for cargo_type.
    """
    await state.update_data(weight=message.text)
    await state.set_state(SendersData.cargo_type)
    await message.answer(
        'Укажите тип посылки',
        reply_markup=await kb.make_inline_keyboard(CARGO_TIPES, 1)
    )
    # добавить шаг про необходимость особого температурного режима
    # (необходимость термопакета или холодильника)


@sender_router.callback_query(SendersData.cargo_type)
async def senders_data_cargo_type(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with cargo_type
    save cargo_type to data
    and send a request for transport.
    """
    await state.update_data(cargo_type=callback.data)
    await callback.message.delete()
    await callback.answer('Ввод предпочитаемого транспорта')
    await state.set_state(SendersData.transport)
    await callback.message.answer(
        'Укажите вид предпочитаемого транспорта',
        reply_markup=await kb.make_inline_keyboard(TRANSPORT, 2)
    )


@sender_router.callback_query(SendersData.transport)
async def senders_data_transport(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with transport
    save transport to data
    and print all sender`s data like a message.
    """
    await state.update_data(transport=callback.data)
    await callback.message.delete()
    await callback.answer('Отображение полученных данных')
    data = await state.get_data()

    if 'type_of_reward_message' in data.keys():
        message = (
            f'Дата отправления: {data["delivery_date"]}\n'
            f'Страна отправления: {data["departure_country"]}\n'
            f'Город отправления: {data["departure_city"]}\n'
            f'Страна прибытия: {data["arrival_country"]}\n'
            f'Город прибытия: {data["arrival_city"]}\n'
            f'Тип вознаграждения: {data["type_of_reward"]}\n'
            f'{data["type_of_reward_message"]}\n'
            f'Размер посылки: {data["size"]}\n'
            f'Масса посылки: {data["weight"]}\n'
            f'Тип посылки: {data["cargo_type"]}\n'
            f'Предпочитаемый транспорт: {data["transport"]}.'
        )
    else:
        message = (
            f'Дата отправления: {data["delivery_date"]}\n'
            f'Страна отправления: {data["departure_country"]}\n'
            f'Город отправления: {data["departure_city"]}\n'
            f'Страна прибытия: {data["arrival_country"]}\n'
            f'Город прибытия: {data["arrival_city"]}\n'
            f'Тип вознаграждения: {data["type_of_reward"]}\n'
            f'{data["type_of_reward_currency"]} '
            f'{data["type_of_reward_value"]}\n'
            f'Размер посылки: {data["size"]}\n'
            f'Масса посылки: {data["weight"]}\n'
            f'Тип посылки: {data["cargo_type"]}\n'
            f'Предпочитаемый транспорт: {data["transport"]}.'
        )

    await callback.message.answer(
        message,
        reply_markup=await kb.make_inline_keyboard(
            ['Редактировать объявление', 'menu'], 1
        )
    )
    # сохранение полученных данны в БД
    await rq.set_sender_add(
        tg_id=callback.from_user.id,
        delivery_date=data["delivery_date"],
        departure_country=data["departure_country"],
        departure_city=data["departure_city"],
        departure_details=data["departure_details"],
        arrival_country=data["arrival_country"],
        arrival_city=data["arrival_city"],
        arrival_details=data["arrival_details"],
        type_of_reward=data["type_of_reward"],
        type_of_reward_currency=data["type_of_reward_currency"],
        type_of_reward_value=data["type_of_reward_value"],
        type_of_reward_message='smth',
        size=data["size"],
        weight=data["weight"],
        cargo_type=data["cargo_type"],
        transport=data["transport"]
        )
    await state.clear()
    await callback.message.answer(
        'Cписок подходящих объявлений',
    )
    # GET запрос в БД сортируем по рейтингу, количеству отзывов,
    # дата отправления (самая ближайшая к дате объявления - самая поздняя)
    # фильтруем по пункт отправления - пункт назначения
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

    # пишем функцию, которая отправит уведомление перевозчику

    # перевозчик получает уведомление с объявлением
    # при нажатии на 'отправить посылку'
    # получаем объект пользователя
    # находим его объявление с активным статусом
    # отправляем сообщение перевозчику и прикладываем сообщение с данными о посылке

    # прилагаем к сообщению кнопки согласится/отказаться

    ## если 'отказаться' - присылаем сообщение с кнопками: укажите, пожалуйста, причину отказа
    ### мой рейс / поездка задерживается
    ### мой рейс / поездка отменилась
    ### содержимое посылки не отвечает требованиям моего объявления
    # / - я не могу обеспечить безопасность сохранность
    # / или содержимое не соответствует требованиям к моему багажу
    ### передумал доставлять

    # отправляем перевозчику сообщение с ником отправителя в телеграм
    # отправляем отправителю сообщение с ником перевозчика в телеграм

    # прикладываем к обоим сообщениям кнопки:

    # посылка успешно доставлена
    ## оставить отзыв об отправителе / о перевозчике
    ### поставьте оценку от 0 до 10, где 10 - великолепно, 0 - никогда не связывайтесь с этим человеком
    ### возможность заполнить текстовое поле

    # не договорились
    ## показываем текстовое поле - напишите пожалуйста, в чем была причина
    ### не сошлись в цене
    ### / заявленное и фактическое содержимое посылки отличаются
    ### / человек не вызывает доверия
    ### / перевозчик отказался доставлять мою посылку

    # передумал отправлять (доставлять)
    # заявить о мошенничестве / нарушениях правил использования бота

    # выбрать другого перевозчика (только для отправителя)
    ## скажите пожалуста в чем причина смены перевозчика
    ## повторяем кнопки и логику: не договорились/мошенничество/передумал
