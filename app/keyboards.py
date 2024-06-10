from datetime import datetime

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from . import calendar

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Хочу отправить',
                callback_data='want_to_send'
            )
        ],
        [
            InlineKeyboardButton(
                text='Хочу доставить',
                callback_data='want_to_delivery'
            )
        ],
        [
            InlineKeyboardButton(
                text='Избранное',
                callback_data='Favorite'
            )
        ],
        [
            InlineKeyboardButton(
                text='Посмотреть историю посылок',
                callback_data='see_orders_history'
            )
        ],
        [
            InlineKeyboardButton(
                text='Посмотреть доступные направления',
                callback_data='see_availible_routes'
            )
        ],
        [
            InlineKeyboardButton(
                text='Сделать донат',
                callback_data='send_money'
            )
        ],
        [
            InlineKeyboardButton(
                text='Написать разработчику',
                callback_data='contact_developer'
            )
        ],
    ]
)


async def years_calendar_keyboard() -> InlineKeyboardMarkup:
    """
    Return InlineKeyboardMarkup with calendar buttons
    for current and next years.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=await calendar.years_calendar_buttons()
    )


async def months_calendar_keyboard() -> InlineKeyboardMarkup:
    """
    Return InlineKeyboardMarkup with calendar buttons for months.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=await calendar.months_calendar_buttons()
    )


async def calendar_keyboard(date: datetime) -> InlineKeyboardMarkup:
    """
    Return InlineKeyboardMarkup with calendar buttons for selected date.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=await calendar.inline_calendar_buttons(date)
    )
