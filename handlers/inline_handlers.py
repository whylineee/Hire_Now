from aiogram import Router, types

from keyboards.reply_keyboards import get_main_keyboard, get_workstation_keyboard
from utils.users import add_new_company, add_new_employee

router = Router()


@router.callback_query(lambda c: c.data.startswith("role_btn_"))
async def test_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "role_btn_employee":
        add_new_employee(callback_query.from_user)
        await callback_query.message.answer(
            "Роль працівника активована. Тепер можете заповнити анкету та шукати вакансії.",
            reply_markup=get_main_keyboard(),
        )
    elif data == "role_btn_company":
        add_new_company(callback_query.from_user)
        await callback_query.message.answer(
            "Роль роботодавця активована. Тепер можете оформити вакансію та шукати кандидатів.",
            reply_markup=get_workstation_keyboard(),
        )

    await callback_query.answer()
