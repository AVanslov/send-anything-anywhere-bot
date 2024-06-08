import calendar
from datetime import datetime

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

inline_keyboard = [
        [
            InlineKeyboardButton(
                text='<<',
                callback_data='Previous_year'
            ),
            InlineKeyboardButton(
                text=str(datetime.now().year),
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='>>',
                callback_data='Next_year'
            )
        ],
        [
            InlineKeyboardButton(
                text='<',
                callback_data='Previous_month'
            ),
            InlineKeyboardButton(
                text=str(calendar.month_abbr[datetime.now().month]),
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='>',
                callback_data='Next_month'
            )
        ],
        [
            InlineKeyboardButton(
                text='Mo',
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='Tu',
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='We',
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='Th',
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='Fr',
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='Sa',
                callback_data='Ignore'
            ),
            InlineKeyboardButton(
                text='Su',
                callback_data='Ignore'
            ),
        ],
    ]


# разберемся с текущим месяцем
# нужно создать список со списками
# строк столько же столько недель в месяце
# в начале и конце месяца могут быть пустые дни - по факту это дни из предыдущего/следующего месяцев
# callback_data должна создержать полностью дату в формате datetime/строки- надо еще подумать что лучше

# Разабъем на шаги решение данной задачи

# Создадим строку из 7 объектов
first_raw = [week_day for week_day in range(1, 8)]

# Узнаем номер дня недели первого дня текущего месяца
number_of_weekday_of_first_day_of_current_month = datetime(
    datetime.now().year, datetime.now().month, 1
).weekday()

# нужна формула, по которой можно получить объект datetime из дня недели
# получить номер дня месяца, где номер не больше 7, а номер дня недели = i

numbers_of_days_in_week = {
    datetime(datetime.now().year, datetime.now().month, day_number).weekday():
    datetime(datetime.now().year, datetime.now().month, day_number)
    for day_number in range(1, 8)
}

# пройдемся в цикле по списку дней недели и сравним порядковый номер дня недели с индексом первого дня
# пока индексы не совпадут, создаем объект с пустой строкой и без действия
first_raw_with_inline_buttons = []

for i, week_day in enumerate(first_raw, 0):

    if i < number_of_weekday_of_first_day_of_current_month:
        text = ' '
        callback_data = 'Ignore'

    elif i == number_of_weekday_of_first_day_of_current_month:
        text = '1'
        callback_data = str(
            datetime(datetime.now().year, datetime.now().month, 1)
        )

    elif i > number_of_weekday_of_first_day_of_current_month:
        text = str(numbers_of_days_in_week[i].day)
        callback_data = str(numbers_of_days_in_week[i])

    first_raw_with_inline_buttons.append(
        InlineKeyboardButton(text=text, callback_data=callback_data)
    )


inline_keyboard.append(first_raw_with_inline_buttons)


# получим номер дня последнего дня 1 недели
# начнем 2 неделю со следующего дня
# также поступим с 3 неделей, 4 и тд.
# если в теущей неделе нет последнего дня месяца или есть, но послдний день месяца - воскресенье:
    # заполняем все дни
# если в текущей неделе есть последний день месяца:
    # то все дни недели с индексом больше чем номер дня недели последнего дня месяца, имеют text = ' ' и callback_data = 'Ignore'


calendar_keyboard = InlineKeyboardMarkup(
    inline_keyboard=inline_keyboard
)
