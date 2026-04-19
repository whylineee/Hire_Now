from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_hs() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Працівник", callback_data="role_btn_employee"),
            InlineKeyboardButton(text="Роботодавець", callback_data="role_btn_company"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
