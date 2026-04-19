from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔎 Шукати вакансії"), KeyboardButton(text="📄 Моя анкета")],
            [KeyboardButton(text="🛠 Редагувати анкету"), KeyboardButton(text="🔄 Змінити роль")],
            [KeyboardButton(text="ℹ️ Про бота"), KeyboardButton(text="💬 Підтримка")],
        ],
        resize_keyboard=True,
    )


def get_quiz_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Моя анкета")],
            [KeyboardButton(text="📸 Оновити фото")],
            [KeyboardButton(text="📝 Опис"), KeyboardButton(text="🛠 Навички")],
            [KeyboardButton(text="📍 Локація"), KeyboardButton(text="💼 Досвід")],
            [KeyboardButton(text="❌ Видалити анкету")],
            [KeyboardButton(text="◀️ Назад до меню")],
        ],
        resize_keyboard=True,
    )


def get_searchion_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏢 Мій кабінет")],
            [KeyboardButton(text="ℹ️ Про бота"), KeyboardButton(text="💬 Підтримка")],
        ],
        resize_keyboard=True,
    )


def get_workstation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👀 Шукати кандидатів"), KeyboardButton(text="🕐 Моя вакансія")],
            [KeyboardButton(text="🛠 Редагувати вакансію"), KeyboardButton(text="🔄 Змінити роль")],
            [KeyboardButton(text="ℹ️ Про бота"), KeyboardButton(text="💬 Підтримка")],
        ],
        resize_keyboard=True,
    )


def get_workstation_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗄 Назва компанії"), KeyboardButton(text="📥 Опис вакансії")],
            [KeyboardButton(text="🔎 Кого шукаєте"), KeyboardButton(text="💲 Зарплатний діапазон")],
            [KeyboardButton(text="📍 Локація компанії"), KeyboardButton(text="🗑 Видалити вакансію")],
            [KeyboardButton(text="◀️ Назад до меню роботодавця")],
        ],
        resize_keyboard=True,
    )
