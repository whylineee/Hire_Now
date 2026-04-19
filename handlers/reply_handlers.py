from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from formatters.cards import (
    format_company_profile_overview,
    format_employee_profile_overview,
)
from keyboards.inline_keyboards import get_inline_hs
from keyboards.reply_keyboards import (
    get_main_keyboard,
    get_quiz_keyboard,
    get_searchion_keyboard,
    get_workstation_keyboard,
    get_workstation_menu_keyboard,
)
from services.marketplace import (
    delete_company,
    delete_employee,
    get_company,
    get_employee,
)
from states.change_skills_py import ChangeSkills
from states.company_states.company_locations import LocationsCompany
from states.company_states.describe_vacancy import DesVacancy
from states.company_states.name_company import NameCompany
from states.company_states.salary_comp import SalaryComp
from states.company_states.search_company import SearchCompany
from states.company_states.who_search_py import WhoSearch
from states.describe_experience import DescribeExperience
from states.edit_user_states import EditDescUser
from states.enter_location import EnterLocations
from states.search_states import SearchEmployee
from states.upload_media_states import UploadMediaStates

router = Router()


EMPLOYEE_MENU_TEXTS = {"📄 Моя анкета", "Моя анкета"}
EMPLOYEE_EDIT_MENU_TEXTS = {"🛠 Редагувати анкету", "📡Анкета📡"}
COMPANY_MENU_TEXTS = {"🕐 Моя вакансія", "🕐Моя вакансія🕐"}
ROLE_MENU_TEXTS = {"🏢 Мій кабінет", "🏢Мій кабінет🏢", "🔄 Змінити роль", "🔹️️️️️️Перемкнути роль"}
ABOUT_TEXTS = {"ℹ️ Про бота", "Про нас", "✏️Про нас✏️", "🤖Про нову версію бота🤖"}
SUPPORT_TEXTS = {"💬 Підтримка", "Підтримка 24/7", "Підтримка 24/7📲"}


@router.message(lambda message: message.text in {"🎮Головне меню", "Головне меню", "◀️ Назад до меню"})
async def show_employee_main_menu(message: types.Message):
    await message.answer("Головне меню працівника", reply_markup=get_main_keyboard())


@router.message(lambda message: message.text in {"Головне меню 💻", "◀️ Назад до меню роботодавця"})
async def show_company_main_menu(message: types.Message):
    await message.answer("Головне меню роботодавця", reply_markup=get_workstation_keyboard())


@router.message(lambda message: message.text in ROLE_MENU_TEXTS)
async def show_role_selector(message: types.Message):
    await message.answer(
        "Виберіть роль. Для кожної ролі бот збереже окрему анкету.",
        reply_markup=get_inline_hs(),
    )


@router.message(lambda message: message.text in ABOUT_TEXTS)
async def show_about(message: types.Message):
    await message.answer(
        "HireNow допомагає кандидатам знаходити релевантні вакансії, а роботодавцям — відповідних людей по навичках і локації.",
        reply_markup=get_searchion_keyboard(),
    )


@router.message(lambda message: message.text in SUPPORT_TEXTS)
async def show_support(message: types.Message):
    await message.answer(
        "Напишіть у підтримку: @whylineee\n\nЯкщо щось не працює, додайте роль, сценарій і короткий опис проблеми.",
        reply_markup=get_searchion_keyboard(),
    )


@router.message(lambda message: message.text in EMPLOYEE_MENU_TEXTS)
async def show_employee_profile(message: types.Message):
    employee = get_employee(message.from_user.id)
    await message.answer(
        format_employee_profile_overview(employee),
        reply_markup=get_quiz_keyboard(),
    )


@router.message(lambda message: message.text in EMPLOYEE_EDIT_MENU_TEXTS)
async def show_employee_edit_menu(message: types.Message):
    employee = get_employee(message.from_user.id)
    await message.answer(
        format_employee_profile_overview(employee),
        reply_markup=get_quiz_keyboard(),
    )


@router.message(lambda message: message.text in COMPANY_MENU_TEXTS)
async def show_company_profile(message: types.Message):
    company = get_company(message.from_user.id)
    await message.answer(
        format_company_profile_overview(company),
        reply_markup=get_workstation_menu_keyboard(),
    )


@router.message(lambda message: message.text == "🔎 Шукати вакансії" or message.text == "🔎Шукати вакансії👁")
async def request_company_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchCompany.company)
    await message.answer(
        "Введіть, що ви шукаєте. Наприклад: `python remote`.\n"
        "Щоб показати все доступне, напишіть `усі`.",
        reply_markup=get_main_keyboard(),
    )


@router.message(lambda message: message.text == "👀 Шукати кандидатів" or message.text == "👷‍♂️Шукати робітників👷‍♂️")
async def request_employee_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchEmployee.query)
    await message.answer(
        "Введіть стек або роль, яку шукаєте. Наприклад: `frontend react kyiv`.\n"
        "Щоб показати всіх, напишіть `усі`.",
        reply_markup=get_workstation_keyboard(),
    )


@router.message(lambda message: message.text == "📝 Опис" or message.text == "📊Поміняти текст📊")
async def request_employee_description(message: types.Message, state: FSMContext):
    await state.set_state(EditDescUser.edit_e_desc)
    await message.answer("Напишіть короткий опис про себе.")


@router.message(lambda message: message.text == "🛠 Навички" or message.text == "🆙Вибрати Технології/Навички🆙")
async def request_employee_skills(message: types.Message, state: FSMContext):
    await state.set_state(ChangeSkills.change_e_skills)
    await message.answer("Введіть навички через кому. Наприклад: Python, Django, PostgreSQL")


@router.message(lambda message: message.text == "💼 Досвід" or message.text == "💻Описати свій досвід роботи в IT💻")
async def request_employee_experience(message: types.Message, state: FSMContext):
    await state.set_state(DescribeExperience.describe_e_experience)
    await message.answer("Опишіть ваш досвід або рівень: Junior / Middle / Senior.")


@router.message(lambda message: message.text == "📍 Локація" or message.text == "📍Ввести локацію роботи📍")
async def request_employee_location(message: types.Message, state: FSMContext):
    await state.set_state(EnterLocations.enter_e_locations)
    await message.answer("Вкажіть місто або формат роботи: Kyiv / Remote / Hybrid.")


@router.message(lambda message: message.text == "📸 Оновити фото" or message.text == "📸Поміняти фото📸")
async def request_employee_photo(message: types.Message, state: FSMContext):
    await state.set_state(UploadMediaStates.wait_for_photo)
    await message.answer("Надішліть фото профілю одним повідомленням.")


@router.message(lambda message: message.text == "🗄 Назва компанії" or message.text == "🗄Назва Компанії🗄")
async def request_company_name(message: types.Message, state: FSMContext):
    await state.set_state(NameCompany.name_c_company)
    await message.answer("Введіть назву компанії.")


@router.message(lambda message: message.text == "📥 Опис вакансії" or message.text == "📥Опис вакансії📥")
async def request_company_description(message: types.Message, state: FSMContext):
    await state.set_state(DesVacancy.des_c_vacancy)
    await message.answer("Опишіть вакансію: стек, задачі, формат роботи.")


@router.message(lambda message: message.text == "🔎 Кого шукаєте" or message.text == "🔎Кого ви шукаєте🔍")
async def request_company_search_role(message: types.Message, state: FSMContext):
    await state.set_state(WhoSearch.who_c_search)
    await message.answer("Кого шукаєте? Наприклад: Python backend developer.")


@router.message(lambda message: message.text == "📍 Локація компанії" or message.text == "📍Локація компанії🚉")
async def request_company_location(message: types.Message, state: FSMContext):
    await state.set_state(LocationsCompany.loc_c_company)
    await message.answer("Вкажіть локацію вакансії: Kyiv / Remote / Hybrid.")


@router.message(lambda message: message.text == "💲 Зарплатний діапазон" or message.text == "💲Зарплатний діпазон💲")
async def request_company_salary(message: types.Message, state: FSMContext):
    await state.set_state(SalaryComp.salary_comp)
    await message.answer("Вкажіть зарплатний діапазон. Наприклад: 2500-3500 USD")


@router.message(lambda message: message.text == "❌ Видалити анкету" or message.text == "❌Видалити анкету❌")
async def remove_employee_profile(message: types.Message):
    deleted = delete_employee(message.from_user.id)
    text = "✅ Анкету працівника видалено." if deleted else "⚠️ Анкету працівника не знайдено."
    await message.answer(text, reply_markup=get_main_keyboard())


@router.message(lambda message: message.text == "🗑 Видалити вакансію" or message.text == "🗑Видалити анкету🗑")
async def remove_company_profile(message: types.Message):
    deleted = delete_company(message.from_user.id)
    text = "✅ Вакансію видалено." if deleted else "⚠️ Вакансію не знайдено."
    await message.answer(text, reply_markup=get_workstation_keyboard())
