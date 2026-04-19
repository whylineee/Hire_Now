from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
EMPLOYEE_PATH = BASE_DIR / "data" / "employee.json"
COMPANY_PATH = BASE_DIR / "data" / "company.json"
LIST_LIMIT = 10

EMPLOYEE_FIELDS = {
    "full_name",
    "username",
    "is_bot",
    "language_code",
    "status",
    "role",
    "profile_img",
    "description",
    "skills",
    "locations",
    "experience",
}

COMPANY_FIELDS = {
    "company_name",
    "username",
    "is_bot",
    "language_code",
    "status",
    "role",
    "description",
    "locations",
    "search",
    "salary",
    "profile_img",
}

FIELD_LABELS = {
    "company_name": "Назва компанії",
    "description": "Опис",
    "experience": "Досвід",
    "locations": "Локація",
    "profile_img": "Фото профілю",
    "salary": "Зарплатний діапазон",
    "search": "Кого шукає компанія",
    "skills": "Навички",
}


def _load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def _save_records(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def normalize_skill_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        raw_items = value
    else:
        raw_items = re.split(r"[,;\n/]+", str(value))

    normalized: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        skill = str(item).strip()
        if not skill:
            continue
        key = skill.casefold()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(skill)
    return normalized


def _normalize_record(record: dict[str, Any], allowed_fields: set[str]) -> dict[str, Any]:
    normalized = {key: value for key, value in record.items() if key in allowed_fields}

    if "skills" in allowed_fields:
        normalized["skills"] = normalize_skill_list(normalized.get("skills"))

    if "locations" in normalized:
        normalized["locations"] = _normalize_text(normalized.get("locations"))
    if "description" in normalized:
        normalized["description"] = _normalize_text(normalized.get("description"))
    if "experience" in normalized:
        normalized["experience"] = _normalize_text(normalized.get("experience"))
    if "search" in normalized:
        normalized["search"] = _normalize_text(normalized.get("search"))
    if "salary" in normalized:
        normalized["salary"] = _normalize_text(normalized.get("salary"))
    if "company_name" in normalized:
        normalized["company_name"] = _normalize_text(normalized.get("company_name"))
    if "profile_img" in normalized:
        normalized["profile_img"] = _normalize_text(normalized.get("profile_img"))

    return normalized


def _build_employee_record(user: Any) -> dict[str, Any]:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "is_bot": user.is_bot,
        "language_code": user.language_code,
        "status": "new",
        "role": "employee",
        "profile_img": None,
        "description": None,
        "skills": [],
        "locations": None,
        "experience": None,
    }


def _build_company_record(user: Any) -> dict[str, Any]:
    return {
        "id": user.id,
        "company_name": None,
        "username": user.username,
        "is_bot": user.is_bot,
        "language_code": user.language_code,
        "status": "new",
        "role": "company",
        "profile_img": None,
        "description": None,
        "locations": None,
        "search": None,
        "salary": None,
    }


def ensure_employee_profile(user: Any) -> dict[str, Any]:
    records = _load_records(EMPLOYEE_PATH)
    existing = next((item for item in records if item.get("id") == user.id), None)
    if existing is None:
        existing = _build_employee_record(user)
        records.append(existing)
    else:
        existing["full_name"] = user.full_name
        existing["username"] = user.username
        existing["language_code"] = user.language_code

    existing = _normalize_record(existing, EMPLOYEE_FIELDS | {"id"})
    for index, item in enumerate(records):
        if item.get("id") == user.id:
            records[index] = existing
            break

    _save_records(EMPLOYEE_PATH, records)
    return existing


def ensure_company_profile(user: Any) -> dict[str, Any]:
    records = _load_records(COMPANY_PATH)
    existing = next((item for item in records if item.get("id") == user.id), None)
    if existing is None:
        existing = _build_company_record(user)
        records.append(existing)
    else:
        existing["username"] = user.username
        existing["language_code"] = user.language_code

    existing = _normalize_record(existing, COMPANY_FIELDS | {"id"})
    for index, item in enumerate(records):
        if item.get("id") == user.id:
            records[index] = existing
            break

    _save_records(COMPANY_PATH, records)
    return existing


def list_employees() -> list[dict[str, Any]]:
    return [_normalize_record(item, EMPLOYEE_FIELDS | {"id"}) for item in _load_records(EMPLOYEE_PATH)]


def list_companies() -> list[dict[str, Any]]:
    return [_normalize_record(item, COMPANY_FIELDS | {"id"}) for item in _load_records(COMPANY_PATH)]


def get_employee(user_id: int) -> dict[str, Any] | None:
    return next((item for item in list_employees() if item.get("id") == user_id), None)


def get_company(user_id: int) -> dict[str, Any] | None:
    return next((item for item in list_companies() if item.get("id") == user_id), None)


def _prepare_value(field: str, new_value: Any) -> Any:
    if field == "skills":
        return normalize_skill_list(new_value)
    return _normalize_text(new_value)


def update_employee_field(user_id: int, field: str, new_value: Any) -> dict[str, Any] | None:
    if field not in EMPLOYEE_FIELDS:
        raise ValueError(f"Unsupported employee field: {field}")

    records = _load_records(EMPLOYEE_PATH)
    for item in records:
        if item.get("id") == user_id:
            item[field] = _prepare_value(field, new_value)
            normalized = _normalize_record(item, EMPLOYEE_FIELDS | {"id"})
            item.update(normalized)
            _save_records(EMPLOYEE_PATH, records)
            return normalized
    return None


def update_company_field(user_id: int, field: str, new_value: Any) -> dict[str, Any] | None:
    if field not in COMPANY_FIELDS:
        raise ValueError(f"Unsupported company field: {field}")

    records = _load_records(COMPANY_PATH)
    for item in records:
        if item.get("id") == user_id:
            item[field] = _prepare_value(field, new_value)
            normalized = _normalize_record(item, COMPANY_FIELDS | {"id"})
            item.update(normalized)
            _save_records(COMPANY_PATH, records)
            return normalized
    return None


def delete_employee(user_id: int) -> bool:
    records = _load_records(EMPLOYEE_PATH)
    filtered = [item for item in records if item.get("id") != user_id]
    if len(filtered) == len(records):
        return False
    _save_records(EMPLOYEE_PATH, filtered)
    return True


def delete_company(user_id: int) -> bool:
    records = _load_records(COMPANY_PATH)
    filtered = [item for item in records if item.get("id") != user_id]
    if len(filtered) == len(records):
        return False
    _save_records(COMPANY_PATH, filtered)
    return True


def get_missing_employee_fields(employee: dict[str, Any] | None) -> list[str]:
    if not employee:
        return ["опис", "навички", "локація", "досвід"]

    missing: list[str] = []
    if not employee.get("description"):
        missing.append("опис")
    if not employee.get("skills"):
        missing.append("навички")
    if not employee.get("locations"):
        missing.append("локація")
    if not employee.get("experience"):
        missing.append("досвід")
    return missing


def get_missing_company_fields(company: dict[str, Any] | None) -> list[str]:
    if not company:
        return ["назва компанії", "опис вакансії", "кого шукаєте", "локація", "зарплата"]

    missing: list[str] = []
    if not company.get("company_name"):
        missing.append("назва компанії")
    if not company.get("description"):
        missing.append("опис вакансії")
    if not company.get("search"):
        missing.append("кого шукаєте")
    if not company.get("locations"):
        missing.append("локація")
    if not company.get("salary"):
        missing.append("зарплата")
    return missing


def field_label(field: str) -> str:
    return FIELD_LABELS.get(field, field)


def _to_tokens(*values: Any) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        if value is None:
            continue
        if isinstance(value, list):
            tokens |= _to_tokens(*value)
            continue
        for token in re.findall(r"[a-zA-Zа-яА-ЯіїєґІЇЄҐ0-9+#._-]+", str(value).casefold()):
            tokens.add(token)
    return tokens


def _score_overlap(left: set[str], right: set[str], weight: int = 1) -> int:
    return len(left & right) * weight


def _score_company(company: dict[str, Any], employee: dict[str, Any] | None, query_tokens: set[str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    company_tokens = _to_tokens(
        company.get("company_name"),
        company.get("description"),
        company.get("locations"),
        company.get("salary"),
        company.get("search"),
    )
    company_skill_tokens = _to_tokens(company.get("search"), company.get("description"))

    if query_tokens:
        query_score = _score_overlap(company_tokens, query_tokens, weight=3)
        if query_score:
            score += query_score
            reasons.append("є збіг з пошуковим запитом")

    if employee:
        skill_tokens = _to_tokens(employee.get("skills"))
        skill_score = _score_overlap(company_skill_tokens, skill_tokens, weight=4)
        if skill_score:
            score += skill_score
            reasons.append("є перетин по навичках")

        employee_locations = _to_tokens(employee.get("locations"))
        location_score = _score_overlap(_to_tokens(company.get("locations")), employee_locations, weight=2)
        if location_score:
            score += location_score
            reasons.append("збігається локація")

        experience_score = _score_overlap(
            _to_tokens(company.get("description"), company.get("search")),
            _to_tokens(employee.get("experience")),
            weight=2,
        )
        if experience_score:
            score += experience_score
            reasons.append("релевантний досвід")

    return score, reasons


def _score_employee(employee: dict[str, Any], company: dict[str, Any] | None, query_tokens: set[str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    employee_tokens = _to_tokens(
        employee.get("full_name"),
        employee.get("description"),
        employee.get("locations"),
        employee.get("experience"),
        employee.get("skills"),
    )

    if query_tokens:
        query_score = _score_overlap(employee_tokens, query_tokens, weight=3)
        if query_score:
            score += query_score
            reasons.append("є збіг з пошуковим запитом")

    if company:
        company_skill_tokens = _to_tokens(company.get("search"), company.get("description"))
        skill_score = _score_overlap(_to_tokens(employee.get("skills")), company_skill_tokens, weight=4)
        if skill_score:
            score += skill_score
            reasons.append("є перетин по навичках")

        location_score = _score_overlap(
            _to_tokens(employee.get("locations")),
            _to_tokens(company.get("locations")),
            weight=2,
        )
        if location_score:
            score += location_score
            reasons.append("збігається локація")

        experience_score = _score_overlap(
            _to_tokens(employee.get("experience"), employee.get("description")),
            _to_tokens(company.get("search"), company.get("description")),
            weight=2,
        )
        if experience_score:
            score += experience_score
            reasons.append("релевантний досвід")

    return score, reasons


def _allow_all(query: str | None) -> bool:
    text = (query or "").strip().casefold()
    return text in {"", "усі", "всі", "all"}


def search_companies_for_employee(user_id: int, query: str | None) -> list[dict[str, Any]]:
    employee = get_employee(user_id)
    query_tokens = _to_tokens(query)
    allow_all = _allow_all(query)
    results: list[dict[str, Any]] = []

    for company in list_companies():
        score, reasons = _score_company(company, employee, query_tokens)
        if not allow_all and score == 0:
            continue
        results.append(
            {
                "item": company,
                "score": score,
                "reasons": reasons,
            }
        )

    results.sort(key=lambda result: (result["score"], bool(result["item"].get("company_name"))), reverse=True)
    return results[:LIST_LIMIT]


def search_employees_for_company(user_id: int, query: str | None) -> list[dict[str, Any]]:
    company = get_company(user_id)
    query_tokens = _to_tokens(query)
    allow_all = _allow_all(query)
    results: list[dict[str, Any]] = []

    for employee in list_employees():
        score, reasons = _score_employee(employee, company, query_tokens)
        if not allow_all and score == 0:
            continue
        results.append(
            {
                "item": employee,
                "score": score,
                "reasons": reasons,
            }
        )

    results.sort(key=lambda result: (result["score"], bool(result["item"].get("skills"))), reverse=True)
    return results[:LIST_LIMIT]
