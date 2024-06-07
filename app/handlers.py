from aiogram import F, html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

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
    await callback.message.answer('Введите желаемую дату доставки')


@router.message(SendersData.delivery_date)
async def senders_data_delivery_date(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with delivery date
    save delivery date to data
    and send a request for departure cauntry.
    """
    await state.update_data(delivery_date=message.text)
    await state.set_state(SendersData.departure_country)
    await message.answer('Укажите страну отправления')


@router.message(SendersData.departure_country)
async def senders_data_departure_country(message: Message, state: FSMContext) -> None:
    """
    This handler recive a message with departure country
    save departure country to data
    and send a request for departure_city.
    """
    await state.update_data(departure_country=message.text)
    data = await state.get_data()
    await message.answer(
        f'Дата отправления: {data["delivery_date"]}\n'
        f'Страна отправления: {data["departure_country"]}.'
    )
    await state.clear()
