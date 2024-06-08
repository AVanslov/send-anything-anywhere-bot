from aiogram import F, html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app import calendar
from app.states import SendersData

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=kb.main_menu
    )


@router.callback_query(F.data == 'want_to_send')
async def send_parcel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    This handler recive calback data 'want_to_send'
    and starts the procedure for creating
    an announcement about the need to send a parcel.
    """
    await callback.answer('Давайте скорее найдем перевозчика для вашего груза')
    await state.set_state(SendersData.delivery_date)
    await callback.message.answer(
        'Выберите желаемую дату доставки',
        reply_markup=calendar.calendar_keyboard
    )


@router.callback_query(SendersData.delivery_date, F.data != 'Ignore')
async def senders_data_delivery_date(callback: CallbackQuery, state: FSMContext) -> None:
    """
    This handler recive a message with delivery date
    save delivery date to data
    and send a request for departure cauntry.
    """
    await state.update_data(delivery_date=callback.data)
    await callback.message.delete()
    await callback.message.answer('Укажите страну отправления')
    await state.set_state(SendersData.departure_country)
    # добавить inline клавиатуру для выбора первой буквы из названия страны
    # добавить inline клавиатуру для выбора страны


@router.message(SendersData.departure_country)
async def senders_data_departure_country(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with departure country
    save departure country to data
    and send a request for departure_city.
    """
    await state.update_data(departure_country=message.text)
    await state.set_state(SendersData.departure_city)
    await message.answer('Укажите город отправления')
    # добавить inline клавиатуру для выбора первой буквы из названия города выбранной страны
    # добавить inline клавиатуру для выбора города


@router.message(SendersData.departure_city)
async def senders_data_departure_city(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with departure_city
    save departure_city to data
    and send a request for arrival_country.
    """
    await state.update_data(departure_city=message.text)
    await state.set_state(SendersData.arrival_country)
    await message.answer('Укажите страну прибытия')


@router.message(SendersData.arrival_country)
async def senders_data_arrival_country(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with arrival_country
    save arrival_country to data
    and send a request for type_of_reward.
    """
    await state.update_data(arrival_country=message.text)
    await state.set_state(SendersData.arrival_city)
    await message.answer('Укажите город прибытия')


@router.message(SendersData.arrival_city)
async def senders_data_arrival_city(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with arrival_city
    save arrival_city to data
    and send a request for type_of_reward.
    """
    await state.update_data(arrival_city=message.text)
    await state.set_state(SendersData.type_of_reward)
    await message.answer('Укажите тип вознаграждения')


@router.message(SendersData.type_of_reward)
async def senders_data_type_of_reward(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with type_of_reward
    save type_of_reward to data
    and send a request for size.
    """
    await state.update_data(type_of_reward=message.text)
    await state.set_state(SendersData.size)
    await message.answer('Укажите размер посылки')


@router.message(SendersData.size)
async def senders_data_size(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with size
    save size to data
    and send a request for weight.
    """
    await state.update_data(size=message.text)
    await state.set_state(SendersData.weight)
    await message.answer('Укажите массу посылки')


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
