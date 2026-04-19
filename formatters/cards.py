from __future__ import annotations

from typing import Any

from services.marketplace import get_missing_company_fields, get_missing_employee_fields


def _display_text(value: Any, default: str = "Не вказано") -> str:
    if value is None:
        return default
    if isinstance(value, list):
        return ", ".join(value) if value else default

    text = str(value).strip()
    return text or default


def format_employee_card(employee: dict[str, Any], *, include_match: bool = False, score: int = 0, reasons: list[str] | None = None) -> str:
    lines = [
        f"👤 {_display_text(employee.get('full_name'))}",
        f"🔖 @{_display_text(employee.get('username'), default='username відсутній')}",
        f"🛠 Навички: {_display_text(employee.get('skills'))}",
        f"💼 Досвід: {_display_text(employee.get('experience'))}",
        f"📍 Локація: {_display_text(employee.get('locations'))}",
        f"📝 Про себе: {_display_text(employee.get('description'))}",
        f"📌 Статус: {_display_text(employee.get('status'))}",
    ]

    if include_match:
        match_details = ", ".join(reasons or []) if reasons else "збіг за базовими параметрами"
        lines.append(f"🎯 Match score: {score}")
        lines.append(f"✅ Чому показано: {match_details}")

    return "\n".join(lines)


def format_company_card(company: dict[str, Any], *, include_match: bool = False, score: int = 0, reasons: list[str] | None = None) -> str:
    lines = [
        f"🏢 Компанія: {_display_text(company.get('company_name'))}",
        f"🔖 @{_display_text(company.get('username'), default='username відсутній')}",
        f"🎯 Шукають: {_display_text(company.get('search'))}",
        f"📍 Локація: {_display_text(company.get('locations'))}",
        f"💲 Зарплата: {_display_text(company.get('salary'))}",
        f"📝 Опис вакансії: {_display_text(company.get('description'))}",
        f"📌 Статус: {_display_text(company.get('status'))}",
    ]

    if include_match:
        match_details = ", ".join(reasons or []) if reasons else "збіг за базовими параметрами"
        lines.append(f"🎯 Match score: {score}")
        lines.append(f"✅ Чому показано: {match_details}")

    return "\n".join(lines)


def format_employee_profile_overview(employee: dict[str, Any] | None) -> str:
    if not employee:
        return "Анкету працівника ще не створено."

    missing = get_missing_employee_fields(employee)
    lines = [
        "📄 Ваша анкета працівника",
        format_employee_card(employee),
    ]
    if missing:
        lines.append(f"⚠️ Ще варто заповнити: {', '.join(missing)}")
    else:
        lines.append("✅ Анкета виглядає заповненою для пошуку.")
    return "\n\n".join(lines)


def format_company_profile_overview(company: dict[str, Any] | None) -> str:
    if not company:
        return "Вакансію роботодавця ще не створено."

    missing = get_missing_company_fields(company)
    lines = [
        "🕐 Ваша вакансія",
        format_company_card(company),
    ]
    if missing:
        lines.append(f"⚠️ Ще варто заповнити: {', '.join(missing)}")
    else:
        lines.append("✅ Вакансія готова до пошуку кандидатів.")
    return "\n\n".join(lines)
