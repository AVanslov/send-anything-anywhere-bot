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
    await state.set_state(CarrierData.delivery_date_year)
    await callback.message.answer(
        'Выберите дату вашей поездки',
        reply_markup=await kb.years_calendar_keyboard()
    )


@carrier_router.callback_query(CarrierData.delivery_date_year)
async def carrier_data_delivery_date_year(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Show Inline buttons with months.
    """
    await state.update_data(delivery_date_year=callback.data)
    await callback.message.delete()
    await callback.answer('Выберите месяц')
    await state.set_state(CarrierData.delivery_date_month)
    data = await state.get_data()
    await callback.message.answer(
        (
            'Выберите дату вашей поездки\nВы выбрали:\nГод - {year}'
        ).format(
            year=data['delivery_date_year'],
        ),
        reply_markup=await kb.months_calendar_keyboard()
    )


@carrier_router.callback_query(CarrierData.delivery_date_month)
async def carrier_data_delivery_date_month(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Show Inline buttons of days for selected year and month.
    """
    await state.update_data(delivery_date_month=callback.data)
    await callback.message.delete()
    await callback.answer('Выберите день')
    await state.set_state(CarrierData.delivery_date)
    data = await state.get_data()
    await callback.message.answer(
        (
            'Выберите дату вашей поездки\nВы выбрали:\n'
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


@carrier_router.callback_query(CarrierData.delivery_date, F.data != IGNORE)
async def carrier_data_delivery_date(
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
    await state.set_state(CarrierData.departure_country_letter)
    await callback.message.answer(
        'Укажите страну отправления',
        # добавляем inline клавиатуру для выбора первой
        # буквы из названия страны
        reply_markup=await kb.make_inline_keyboard(ALPHABET_EN, 4)
    )


@carrier_router.callback_query(CarrierData.departure_country_letter)
async def carrier_data_departure_country_letter(
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
    await state.set_state(CarrierData.departure_country)
    data = await state.get_data()
    await callback.message.answer(
        'Укажите страну отправления',
        reply_markup=await kb.countries(data['departure_country_letter'])
    )


@carrier_router.callback_query(CarrierData.departure_country)
async def carrier_data_departure_country(
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
    await state.set_state(CarrierData.departure_city)
    data = await state.get_data()
    await callback.message.answer(
        'Укажите город отправления',
        reply_markup=await kb.cities(data['departure_country'])
    )


@carrier_router.callback_query(CarrierData.departure_city)
async def senders_data_departure_details(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler recive a message with departure_city
    save departure_city to data
    and send a request for arrival_country.
    """
    await state.update_data(departure_city=callback.data)
    await state.set_state(CarrierData.arrival_country_letter)
    await callback.message.answer(
        'Укажите страну прибытия',
        reply_markup=await kb.make_inline_keyboard(ALPHABET_EN, 4)
    )


@carrier_router.callback_query(CarrierData.arrival_country_letter)
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
    await state.set_state(CarrierData.arrival_country)
    data = await state.get_data()
    await callback.message.answer(
        'Укажите страну прибытия',
        reply_markup=await kb.countries(data['arrival_country_letter'])
    )


@carrier_router.callback_query(CarrierData.arrival_country)
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
    await state.set_state(CarrierData.arrival_city)
    data = await state.get_data()
    # оценка количества городов
    # если городов более 20,
    # показываем алфавитную клавиатуру для выбора города / пагинацию
    await callback.message.answer(
        'Укажите город прибытия',
        reply_markup=await kb.cities(data['arrival_country'])
    )


@carrier_router.callback_query(CarrierData.arrival_city)
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
    await callback.answer('Укажите тип вознаграждения.')
    await state.set_state(CarrierData.type_of_reward)
    await callback.message.answer(
        'Укажите тип вознаграждения',
        reply_markup=await kb.type_of_reward()
    )


@carrier_router.callback_query(CarrierData.type_of_reward, F.data == 'money')
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
    await state.set_state(CarrierData.type_of_reward_currency)
    await callback.message.answer(
        'Выберите валюту',
        reply_markup=await kb.make_inline_keyboard(CURRENCIES, 2)
    )


@carrier_router.callback_query(CarrierData.type_of_reward_currency)
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
    await state.set_state(CarrierData.type_of_reward_value)
    await callback.message.answer('Укажите сумму вознаграждения')


@carrier_router.callback_query(CarrierData.type_of_reward, F.data == 'other')
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
    await state.set_state(CarrierData.type_of_reward_message)
    await callback.message.answer(
        'Укажите комментарий к вознагрождению, например:'
        '"по договорённости",'
        '"за коробку конфет",'
        '"бесплатно"'
        'и ид. и т.п.'
    )


@carrier_router.message(CarrierData.type_of_reward_message)
async def senders_data_type_of_reward_message(
    message: Message, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward_message
    save type_of_reward_message to data
    and send a request for size.
    """
    await state.update_data(type_of_reward_message=message.text)
    await state.set_state(CarrierData.size)
    await message.answer(
        'Укажите габариты посылки',
        reply_markup=await kb.make_inline_keyboard(SIZE, 1)
    )


@carrier_router.message(CarrierData.type_of_reward_value)
async def senders_data_type_of_reward_value(
    message: Message, state: FSMContext
) -> None:
    """
    This handler recive a message with type_of_reward_value
    save type_of_reward_value to data
    and send a request for size.
    """
    await state.update_data(type_of_reward_value=message.text)
    await state.set_state(CarrierData.size)
    await message.answer(
        'Укажите габариты посылки',
        reply_markup=await kb.make_inline_keyboard(SIZE, 1)
    )


@carrier_router.callback_query(CarrierData.size)
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
    await state.set_state(CarrierData.weight)
    await callback.message.answer('Укажите массу посылки в кг.')


@carrier_router.message(CarrierData.weight)
async def senders_data_weight(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with weight
    save weight to data
    and send a request for cargo_type.
    """
    await state.update_data(weight=message.text)
    await state.set_state(CarrierData.cargo_type)
    await message.answer(
        'Укажите тип посылки',
        reply_markup=await kb.make_inline_keyboard(CARGO_TIPES, 1)
    )
    # добавить шаг про необходимость особого температурного режима
    # (необходимость термопакета или холодильника)


@carrier_router.callback_query(CarrierData.cargo_type)
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
    await state.set_state(CarrierData.transport)
    await callback.message.answer(
        'Укажите вид предпочитаемого транспорта',
        reply_markup=await kb.make_inline_keyboard(TRANSPORT, 2)
    )


@carrier_router.callback_query(CarrierData.transport)
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
            f'Транспорт: {data["transport"]}.'
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
            f'Транспорт: {data["transport"]}.'
        )

    # сохранение полученных данны в БД
    await callback.message.answer(
        message,
        reply_markup=await kb.make_inline_keyboard(
            ['Редактировать объявление'], 2  # запрос в БД на редактирование
        )
    )
    await state.clear()
    await callback.message.answer(
        'Cписок подходящих объявлений.\n'
        'Подходящие объявления не найдены,'
        'Нажмите кнопку ниже "Подписаться"'
        'и мы пришлем вам релевантные объявления, как только они появятся',
    )
