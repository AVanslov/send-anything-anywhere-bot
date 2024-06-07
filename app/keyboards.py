from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

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
