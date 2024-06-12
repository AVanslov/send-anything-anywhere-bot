from datetime import datetime

from aiogram import F, html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.constants import (
    ALPHABET_EN,
    CURRENCIES,
    # ALPHABET_RU,
    IGNORE,
)
import app.keyboards as kb
from app.states import SendersData

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=await kb.main_menu()
    )


@router.callback_query(F.data == 'want_to_send')
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


@router.callback_query(SendersData.delivery_date_year)
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


@router.callback_query(SendersData.delivery_date_month)
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


@router.callback_query(SendersData.delivery_date, F.data != IGNORE)
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
    # добавляем inline клавиатуру для выбора страны


@router.callback_query(SendersData.departure_country_letter)
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


@router.callback_query(SendersData.departure_country)
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


@router.callback_query(SendersData.departure_city)
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


@router.message(SendersData.departure_details)
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


@router.callback_query(SendersData.arrival_country_letter)
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


@router.callback_query(SendersData.arrival_country)
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
    await callback.message.answer(
        'Укажите город прибытия',
        reply_markup=await kb.cities(data['arrival_country'])
    )


@router.callback_query(SendersData.arrival_city)
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
        'eсть ли доп. требования: отправить по почте, передать в аэропорту и тд. и тп.'
    )


@router.message(SendersData.arrival_details)
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
    # Показываем выбор типа
        # деньги
            # показываем выбор валюты
            # показываем поле ввода цифр
        # Другое
            # показываем текстовое поле


@router.callback_query(SendersData.type_of_reward, F.data == 'money')
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


@router.callback_query(SendersData.type_of_reward_currency)
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


@router.callback_query(SendersData.type_of_reward, F.data == 'other')
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


@router.message(SendersData.type_of_reward_message)
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
    await message.answer('Укажите габариты посылки')
    # добавить понятные варианты:
    # XL - не больше 600 x 350 x 300 mm
    # L - не больше 310 x 250 x 380 mm
    # M - не больше 330 x 250 x 155 mm
    # XS - не больше 170 x 120 x 90 mm
    # S - не больше 220 x 200 x 110 mm
    # конверт А2 - не больше 495 x 580 x 50 mm
    # конверт А3 - не больше 350 x 420 x 50 mm
    # конверт А4 - не больше 260 x 340 x 50 mm
    # конверт А5 - не больше 149 x 210 x 50 mm


@router.message(SendersData.type_of_reward_value)
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
    await message.answer('Укажите габариты посылки')
    # добавить понятные варианты:
    # XL - не больше 600 x 350 x 300 mm
    # L - не больше 310 x 250 x 380 mm
    # M - не больше 330 x 250 x 155 mm
    # XS - не больше 170 x 120 x 90 mm
    # S - не больше 220 x 200 x 110 mm
    # конверт А2 - не больше 495 x 580 x 50 mm
    # конверт А3 - не больше 350 x 420 x 50 mm
    # конверт А4 - не больше 260 x 340 x 50 mm
    # конверт А5 - не больше 149 x 210 x 50 mm


@router.message(SendersData.size)
async def senders_data_size(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with size
    save size to data
    and send a request for weight.
    """
    await state.update_data(size=message.text)
    await state.set_state(SendersData.weight)
    await message.answer('Укажите массу посылки в кг.')


@router.message(SendersData.weight)
async def senders_data_weight(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with weight
    save weight to data
    and send a request for cargo_type.
    """
    await state.update_data(weight=message.text)
    await state.set_state(SendersData.cargo_type)
    await message.answer('Укажите тип посылки')
    # документы
    # личные вещи
    # одежда
    # бытовая химия
    # бьющиеся и хрупкие предметы
    # продукты питания
    # лекарства
    # прочие предметы
    # добавить шаг про необходимость особого температурного режима
    # (необходимость термопакета или холодильника)

@router.message(SendersData.cargo_type)
async def senders_data_cargo_type(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with cargo_type
    save cargo_type to data
    and send a request for transport.
    """
    await state.update_data(cargo_type=message.text)
    await state.set_state(SendersData.transport)
    await message.answer('Укажите вид предпочитаемого транспорта')


@router.message(SendersData.transport)
async def senders_data_transport(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with transport
    save transport to data
    and print all sender`s data like a message.
    """
    await state.update_data(transport=message.text)
    data = await state.get_data()
    await message.answer(
        f'Дата отправления: {data["delivery_date"]}\n'
        f'Страна отправления: {data["departure_country"]}\n'
        f'Город отправления: {data["departure_city"]}\n'
        f'Страна прибытия: {data["arrival_country"]}\n'
        f'Город прибытия: {data["arrival_city"]}\n'
        f'Тип вознаграждения: {data["type_of_reward"]}\n'
        f'Размер посылки: {data["size"]}\n'
        f'Масса посылки: {data["weight"]}\n'
        f'Тип посылки: {data["cargo_type"]}\n'
        f'Предпочитаемый транспорт: {data["transport"]}.'
    )
    await state.clear()
