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
    datetime.now().year,
    datetime.now().month,
    1
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
used_day_numbers = []

for i, week_day in enumerate(first_raw, 0):

    if i < number_of_weekday_of_first_day_of_current_month:
        text = ' '
        callback_data = 'Ignore'

    elif i == number_of_weekday_of_first_day_of_current_month:
        text = 1
        callback_data = datetime(datetime.now().year, datetime.now().month, 1)

    elif i > number_of_weekday_of_first_day_of_current_month:
        text = numbers_of_days_in_week[i].day
        callback_data = numbers_of_days_in_week[i]

    if callback_data != 'Ignore':
        used_day_numbers.append(callback_data)

    first_raw_with_inline_buttons.append(
        InlineKeyboardButton(text=str(text), callback_data=str(callback_data))
    )


inline_keyboard.append(first_raw_with_inline_buttons)


# цикл для каждой недели
for i in range(1, 6):
    raw_with_inline_buttons = []

    # получим номер последнего дня текущей недели
    used_day_numbers[-1]
    # начнем следующую неделю со следующего дня
    used_day_numbers[-1].day + 1
    # также поступим с 3 неделей, 4 и тд.

    # получим последний день текущего месяца / количество дней в месяце

    count_of_days_in_current_month = calendar.monthrange(
        datetime.now().year,
        datetime.now().month
    )[1]

    # если в теущей неделе нет последнего дня месяца или есть, но последний день месяца - воскресенье:

    for day_number in range(
        # получим номер дня понедельника на основе последнего дня предыдущей недели
        used_day_numbers[-1].day + 1,
        # получим номер дня воскресенья
        used_day_numbers[-1].day + 8
    ):
        # ограничим цикл только существующими числами месяца
        if day_number <= count_of_days_in_current_month:
            # условие, что в этом диапазоне нет номера == последний день месяца или есть, но его индекс 7 - воскресенье:
            if datetime(
                datetime.now().year,
                datetime.now().month,
                count_of_days_in_current_month
            ) not in [
                datetime(datetime.now().year, datetime.now().month, day)
                for day in range(
                    used_day_numbers[-1].day + 1, used_day_numbers[-1].day + 8
                ) if day <= count_of_days_in_current_month
            ] or (
                datetime(
                    datetime.now().year,
                    datetime.now().month,
                    count_of_days_in_current_month
                ) in [
                    datetime(datetime.now().year, datetime.now().month, day)
                    for day in range(
                        used_day_numbers[-1].day + 1,
                        used_day_numbers[-1].day + 8
                    ) if day <= count_of_days_in_current_month
                ]
                and datetime(
                    datetime.now().year,
                    datetime.now().month,
                    count_of_days_in_current_month
                ).weekday() == 7
            ):
                # заполняем все дни
                text = datetime(datetime.now().year, datetime.now().month, day_number).day
                callback_data = datetime(datetime.now().year, datetime.now().month, day_number)

                used_day_numbers.append(callback_data)

            # если в текущей неделе есть последний день месяца:
                # то все дни недели с индексом больше,
                # чем номер дня недели последнего дня месяца,
                # имеют text = ' ' и callback_data = 'Ignore'
            elif (
                datetime(
                    datetime.now().year,
                    datetime.now().month,
                    count_of_days_in_current_month
                ) in [
                    datetime(
                        datetime.now().year,
                        datetime.now().month,
                        day
                    ) for day in range(
                        used_day_numbers[-1].day + 1,
                        used_day_numbers[-1].day + 8
                    ) if day <= count_of_days_in_current_month
                ]
            ) and (
                datetime(
                    datetime.now().year,
                    datetime.now().month,
                    day_number
                ).weekday() != datetime(
                    datetime.now().year,
                    datetime.now().month,
                    count_of_days_in_current_month
                ).weekday() + 1
            ):
                text = datetime(
                    datetime.now().year,
                    datetime.now().month,
                    day_number
                ).day
                callback_data = datetime(
                    datetime.now().year,
                    datetime.now().month,
                    day_number
                )

                used_day_numbers.append(callback_data)

            else:
                text = ' '
                callback_data = 'Ignore'

            raw_with_inline_buttons.append(
                InlineKeyboardButton(
                    text=str(text),
                    callback_data=str(callback_data)
                )
            )

    inline_keyboard.append(raw_with_inline_buttons)


calendar_keyboard = InlineKeyboardMarkup(
    inline_keyboard=inline_keyboard
)
