from __future__ import annotations

from formatters.cards import format_company_card, format_employee_card
from services.marketplace import (
    ensure_company_profile,
    ensure_employee_profile,
    field_label,
    get_company,
    get_employee,
    update_company_field,
    update_employee_field,
)


def add_new_employee(data):
    return ensure_employee_profile(data)


def add_new_company(data):
    return ensure_company_profile(data)


def edit_field_company(msg, field, value):
    company = update_company_field(msg.from_user.id, field, value["new_value"])
    if not company:
        return "Спочатку оберіть роль роботодавця та створіть вакансію."

    return (
        f"✅ Поле «{field_label(field)}» оновлено.\n\n"
        f"{format_company_card(company)}"
    )


def edit_field_employee(msg, field, value):
    employee = update_employee_field(msg.from_user.id, field, value["new_value"])
    if not employee:
        return "Спочатку оберіть роль працівника та створіть анкету."

    return (
        f"✅ Поле «{field_label(field)}» оновлено.\n\n"
        f"{format_employee_card(employee)}"
    )


def get_employee_text(employee):
    return format_employee_card(employee)


def get_company_text(company):
    return format_company_card(company)


def get_employee_profile(user_id: int):
    return get_employee(user_id)


def get_company_profile(user_id: int):
    return get_company(user_id)
