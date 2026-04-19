import os

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from formatters.cards import format_company_card, format_employee_card
from keyboards.reply_keyboards import get_main_keyboard, get_workstation_keyboard
from services.marketplace import (
    get_company,
    get_employee,
    search_companies_for_employee,
    search_employees_for_company,
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
from utils.users import edit_field_company, edit_field_employee

router = Router()


@router.message(EditDescUser.edit_e_desc)
async def edit_desc_handler(message: types.Message, state: FSMContext):
    await state.update_data(edit_desc=message.text)
    data = await state.get_data()
    msg_text = edit_field_employee(message, "description", {"new_value": data["edit_desc"]})
    await message.answer(msg_text, reply_markup=get_main_keyboard())
    await state.clear()


@router.message(SearchEmployee.query)
async def search_candidates(message: types.Message, state: FSMContext):
    results = search_employees_for_company(message.from_user.id, message.text)
    company = get_company(message.from_user.id)
    await state.clear()

    if not company:
        await message.answer(
            "Спочатку оберіть роль роботодавця і заповніть вакансію, щоб пошук був точнішим.",
            reply_markup=get_workstation_keyboard(),
        )
        return

    if not results:
        await message.answer(
            "Нікого не знайшов. Спробуйте інший запит або заповніть поле «кого шукаєте» у вакансії.",
            reply_markup=get_workstation_keyboard(),
        )
        return

    await message.answer(f"Знайшов {len(results)} кандидатів:", reply_markup=get_workstation_keyboard())
    for result in results:
        employee = result["item"]
        caption = format_employee_card(
            employee,
            include_match=True,
            score=result["score"],
            reasons=result["reasons"],
        )
        profile_img = employee.get("profile_img")
        if profile_img and os.path.exists(profile_img):
            await message.answer_photo(FSInputFile(profile_img), caption=caption)
        else:
            await message.answer(caption)


@router.message(ChangeSkills.change_e_skills)
async def change_e_skills(message: types.Message, state: FSMContext):
    await state.update_data(change_skills=message.text)
    data = await state.get_data()
    txt = edit_field_employee(message, "skills", {"new_value": data["change_skills"]})
    await message.answer(txt, reply_markup=get_main_keyboard())
    await state.clear()


@router.message(EnterLocations.enter_e_locations)
async def enter_e_locations(message: types.Message, state: FSMContext):
    await state.update_data(enter_locations=message.text)
    data = await state.get_data()
    txt = edit_field_employee(message, "locations", {"new_value": data["enter_locations"]})
    await message.answer(txt, reply_markup=get_main_keyboard())
    await state.clear()


@router.message(DescribeExperience.describe_e_experience)
async def describe_e_experience(message: types.Message, state: FSMContext):
    await state.update_data(describe_experience=message.text)
    data = await state.get_data()
    txt = edit_field_employee(message, "experience", {"new_value": data["describe_experience"]})
    await message.answer(txt, reply_markup=get_main_keyboard())
    await state.clear()


@router.message(UploadMediaStates.wait_for_photo)
async def photo_handler(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Потрібно надіслати саме фото.")
        return

    photo = message.photo[-1]
    destination_folder = "media"
    os.makedirs(destination_folder, exist_ok=True)
    file_path = os.path.join(destination_folder, f"{photo.file_unique_id}.jpg")
    file_info = await message.bot.get_file(photo.file_id)
    await message.bot.download_file(file_info.file_path, destination=file_path)

    msg_text = edit_field_employee(message, "profile_img", {"new_value": file_path})
    employee = get_employee(message.from_user.id)
    await message.answer(msg_text, reply_markup=get_main_keyboard())

    if employee and employee.get("profile_img") and os.path.exists(employee["profile_img"]):
        await message.answer_photo(
            photo=FSInputFile(employee["profile_img"]),
            caption="Фото профілю оновлено.",
        )

    await state.clear()


@router.message(NameCompany.name_c_company)
async def name_c_company(message: types.Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    data = await state.get_data()
    txt = edit_field_company(message, "company_name", {"new_value": data["company_name"]})
    await message.answer(txt, reply_markup=get_workstation_keyboard())
    await state.clear()


@router.message(DesVacancy.des_c_vacancy)
async def describe_vacancy(message: types.Message, state: FSMContext):
    await state.update_data(des_vacancy=message.text)
    data = await state.get_data()
    txt = edit_field_company(message, "description", {"new_value": data["des_vacancy"]})
    await message.answer(txt, reply_markup=get_workstation_keyboard())
    await state.clear()


@router.message(WhoSearch.who_c_search)
async def who_search(message: types.Message, state: FSMContext):
    await state.update_data(who_search=message.text)
    data = await state.get_data()
    txt = edit_field_company(message, "search", {"new_value": data["who_search"]})
    await message.answer(txt, reply_markup=get_workstation_keyboard())
    await state.clear()


@router.message(LocationsCompany.loc_c_company)
async def company_locations(message: types.Message, state: FSMContext):
    await state.update_data(enter_c_locations=message.text)
    data = await state.get_data()
    txt = edit_field_company(message, "locations", {"new_value": data["enter_c_locations"]})
    await message.answer(txt, reply_markup=get_workstation_keyboard())
    await state.clear()


@router.message(SalaryComp.salary_comp)
async def salary_comp(message: types.Message, state: FSMContext):
    await state.update_data(enter_salary=message.text)
    data = await state.get_data()
    txt = edit_field_company(message, "salary", {"new_value": data["enter_salary"]})
    await message.answer(txt, reply_markup=get_workstation_keyboard())
    await state.clear()


@router.message(SearchCompany.company)
async def search_vacancies(message: types.Message, state: FSMContext):
    results = search_companies_for_employee(message.from_user.id, message.text)
    employee = get_employee(message.from_user.id)
    await state.clear()

    if not employee:
        await message.answer(
            "Спочатку оберіть роль працівника і заповніть анкету, щоб пошук був точнішим.",
            reply_markup=get_main_keyboard(),
        )
        return

    if not results:
        await message.answer(
            "Не знайшов релевантних вакансій. Спробуйте інший запит або доповніть навички в анкеті.",
            reply_markup=get_main_keyboard(),
        )
        return

    await message.answer(f"Знайшов {len(results)} вакансій:", reply_markup=get_main_keyboard())
    for result in results:
        await message.answer(
            format_company_card(
                result["item"],
                include_match=True,
                score=result["score"],
                reasons=result["reasons"],
            )
        )
