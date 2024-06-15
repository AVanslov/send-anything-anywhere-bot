from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

menu_router = Router()


@menu_router.callback_query(F.data == 'menu')
async def menu_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    This handler receives `menu` data
    return maim menu buttons.
    """
    await callback.answer('Вы вернулись в главное меню')
    try:
        await state.clear()
    except Exception():
        raise Exception(
            'В предыдущих шагах не было'
            'определено состояние - состояние не очищено.'
        )
    await callback.message.answer(
        'It`s the main menu.',
        reply_markup=await kb.main_menu()
    )
