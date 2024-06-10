import calendar
from datetime import datetime

from aiogram.types import (
    InlineKeyboardButton,
)

from .constants import (
    IGNORE,
)


async def years_calendar_buttons() -> list:
    """
    Return keyboards with current and next year.
    """
    return [
        [
            InlineKeyboardButton(
                text=str(datetime.now().year),
                callback_data=str(datetime.now().year)
            ),
            InlineKeyboardButton(
                text=str(datetime.now().year + 1),
                callback_data=str(datetime.now().year + 1)
            ),
        ]
    ]


async def months_calendar_buttons() -> list:
    """
    Return keyboards with months of selected year.
    """
    return [
        [
            InlineKeyboardButton(
                text=str(calendar.month_abbr[column+1*raw]),
                callback_data=str(column+1*raw)
            ) for column in range(1, 4)
        ] for raw in [0, 3, 6, 9]
    ]


async def inline_calendar_buttons(date: datetime) -> list:
    """
    Recive an object of datetime,
    Return a Calendar view of corresponding month as an InlineKeyboard.
    """

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=str(date.year),
                callback_data=IGNORE
            ),
        ],
        [
            InlineKeyboardButton(
                text=str(calendar.month_abbr[date.month]),
                callback_data=IGNORE
            ),
        ],
        [
            InlineKeyboardButton(
                text='Mo',
                callback_data=IGNORE
            ),
            InlineKeyboardButton(
                text='Tu',
                callback_data=IGNORE
            ),
            InlineKeyboardButton(
                text='We',
                callback_data=IGNORE
            ),
            InlineKeyboardButton(
                text='Th',
                callback_data=IGNORE
            ),
            InlineKeyboardButton(
                text='Fr',
                callback_data=IGNORE
            ),
            InlineKeyboardButton(
                text='Sa',
                callback_data=IGNORE
            ),
            InlineKeyboardButton(
                text='Su',
                callback_data=IGNORE
            ),
        ],
    ]
# узнаем номер дня недели первого дня месяца
    number_of_weekday_of_first_day_of_current_month = datetime(
        date.year,
        date.month,
        1
    ).weekday()
# Узнаем количество дней в текущем месяце
    count_of_days_in_current_month = calendar.monthrange(
        date.year,
        date.month
    )[1]
# узнаем номер дня недели последнего дня месяца
    number_of_weekday_of_last_day_of_current_month = datetime(
        date.year,
        date.month,
        count_of_days_in_current_month,
    ).weekday()
# формируем список от 1 до количества дней в месяце
    all_days_in_month = [
        i for i in range(
            1,
            count_of_days_in_current_month + 1
        )
    ]
# добавляем в начало количество = номеру недели первого дня месяца
    for i in range(1, number_of_weekday_of_first_day_of_current_month + 1):
        all_days_in_month.insert(0, ' ')
# добавляем в конец количество = 7 - номер дня недели последнего дня месяца
    for i in range(1, 8 - number_of_weekday_of_last_day_of_current_month):
        all_days_in_month.append(' ')
# делим список на подсписки
    raw_with_inline_buttons = [
            [
                InlineKeyboardButton(
                    text=str(date),
                    callback_data=IGNORE
                ) if date == ' ' else
                # добавляем к inline_keyboard список с подсписками
                # у добавленных дней с указываем callback_data = 'Ignore'
                InlineKeyboardButton(
                    text=str(date),
                    callback_data=str(date)
                ) for date in all_days_in_month[i:i + 7]
            ] for i in range(0, len(all_days_in_month), 7)
        ]

    for i in raw_with_inline_buttons:
        inline_keyboard.append(i)

    return inline_keyboard
