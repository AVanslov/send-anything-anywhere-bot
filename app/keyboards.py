from datetime import datetime
import json

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


async def make_inline_keyboard(data: list, raws: int) -> InlineKeyboardMarkup:
    """
    Receives a list as input and divides it into lists
    by the specified number of elements,
    then forms a keyboard layout object in the form of a grid.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i,
                    callback_data=i
                ) for i in data[i:i + raws]
            ] for i in range(0, len(data), raws)
        ]
    )


async def countries(first_letter: str) -> InlineKeyboardMarkup:
    # фильтруем список ключей из json со странами
    # и городами по первой букве ключа
    with open("all_countries_and_cities.json", "r") as fh:
        countries_and_cities = json.load(fh)
    countries = [i for i in countries_and_cities.keys()]
    return await make_inline_keyboard(
        [i for i in countries if i[:1] == first_letter], 2
    )


async def cities(country: str) -> InlineKeyboardMarkup:
    with open("all_countries_and_cities.json", "r") as fh:
        countries_and_cities = json.load(fh)
    for key, cities_of_current_country in countries_and_cities.items():
        if key == country:
            return await make_inline_keyboard(
                [i for i in cities_of_current_country], 2
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
