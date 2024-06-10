import calendar
from datetime import datetime

from aiogram.types import (
    InlineKeyboardButton,
)

from .constants import (
    IGNORE,
    NEXT_YEAR,
    NEXT_MONTH,
    PREVIOUS_YEAR,
    PREVIOUS_MONTH,
    YEARS,
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
                text=str(calendar.month_abbr[month_number]),
                callback_data=str(month_number)
            )
        ] for month_number in range(1, 12)
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
        date.year,
        date.month,
        1
    ).weekday()

    # нужна формула, по которой можно получить объект datetime из дня недели
    # получить номер дня месяца, где номер не больше 7, а номер дня недели = i

    numbers_of_days_in_week = {
        datetime(date.year, date.month, day_number).weekday():
        datetime(date.year, date.month, day_number)
        for day_number in range(1, 8)
    }

    # пройдемся в цикле по списку дней недели и сравним порядковый номер дня недели с индексом первого дня
    # пока индексы не совпадут, создаем объект с пустой строкой и без действия
    first_raw_with_inline_buttons = []
    used_day_numbers = []

    for i, week_day in enumerate(first_raw, 0):

        if i < number_of_weekday_of_first_day_of_current_month:
            text = ' '
            callback_data = IGNORE

        elif i == number_of_weekday_of_first_day_of_current_month:
            text = 1
            callback_data = datetime(date.year, date.month, 1)

        elif i > number_of_weekday_of_first_day_of_current_month:
            text = numbers_of_days_in_week[i].day
            callback_data = numbers_of_days_in_week[i]

        if callback_data != IGNORE:
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
            date.year,
            date.month
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
                    date.year,
                    date.month,
                    count_of_days_in_current_month
                ) not in [
                    datetime(date.year, date.month, day)
                    for day in range(
                        used_day_numbers[-1].day + 1, used_day_numbers[-1].day + 8
                    ) if day <= count_of_days_in_current_month
                ] or (
                    datetime(
                        date.year,
                        date.month,
                        count_of_days_in_current_month
                    ) in [
                        datetime(date.year, date.month, day)
                        for day in range(
                            used_day_numbers[-1].day + 1,
                            used_day_numbers[-1].day + 8
                        ) if day <= count_of_days_in_current_month
                    ]
                    and datetime(
                        date.year,
                        date.month,
                        count_of_days_in_current_month
                    ).weekday() == 7
                ):
                    # заполняем все дни
                    text = datetime(date.year, date.month, day_number).day
                    callback_data = datetime(date.year, date.month, day_number)

                    used_day_numbers.append(callback_data)

                # если в текущей неделе есть последний день месяца:
                    # то все дни недели с индексом больше,
                    # чем номер дня недели последнего дня месяца,
                    # имеют text = ' ' и callback_data = IGNORE
                elif (
                    datetime(
                        date.year,
                        date.month,
                        count_of_days_in_current_month
                    ) in [
                        datetime(
                            date.year,
                            date.month,
                            day
                        ) for day in range(
                            used_day_numbers[-1].day + 1,
                            used_day_numbers[-1].day + 8
                        ) if day <= count_of_days_in_current_month
                    ]
                ) and (
                    datetime(
                        date.year,
                        date.month,
                        day_number
                    ).weekday() != datetime(
                        date.year,
                        date.month,
                        count_of_days_in_current_month
                    ).weekday() + 1
                ):
                    text = datetime(
                        date.year,
                        date.month,
                        day_number
                    ).day
                    callback_data = datetime(
                        date.year,
                        date.month,
                        day_number
                    )

                    used_day_numbers.append(callback_data)

                else:
                    text = ' '
                    callback_data = IGNORE

                raw_with_inline_buttons.append(
                    InlineKeyboardButton(
                        text=str(text),
                        callback_data=str(callback_data)
                    )
                )

        inline_keyboard.append(raw_with_inline_buttons)

    return inline_keyboard
