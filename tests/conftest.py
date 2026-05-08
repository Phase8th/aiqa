import json
import os
from pathlib import Path
from datetime import datetime
import uuid

import pytest
import allure
from jsonschema import Draft202012Validator, FormatChecker
from playwright.sync_api import expect


API_EPIC = "AIQA"
API_FEATURE = "Урок 4: API HTTP-тренажёра"
UI_EPIC = "AIQA"
UI_FEATURE = "Урок 4: UI HTTP-тренажёра"


USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "role", "created_at", "updated_at"],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "role": {"type": "string", "enum": ["viewer", "editor", "admin"]},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": False,
}

USER_LIST_SCHEMA = {
    "type": "object",
    "required": ["items", "total", "session"],
    "properties": {
        "items": {"type": "array", "items": USER_SCHEMA},
        "total": {"type": "integer", "minimum": 0},
        "session": {"type": "string", "minLength": 1, "maxLength": 128},
    },
    "additionalProperties": False,
}

ERROR_SCHEMA = {
    "type": "object",
    "required": ["error"],
    "properties": {
        "error": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}

STATUS_CODE_RESPONSE_SCHEMA = {
    "oneOf": [
        {
            "type": "object",
            "required": ["code", "name", "category", "description", "qa_note"],
            "properties": {
                "code": {"type": "integer"},
                "name": {"type": "string", "minLength": 1},
                "category": {"type": "string", "minLength": 1},
                "description": {"type": "string", "minLength": 1},
                "qa_note": {"type": "string", "minLength": 1},
            },
            "additionalProperties": False,
        },
        {
            "type": "object",
            "required": ["status", "title", "category", "description", "qa_note"],
            "properties": {
                "status": {"type": "integer"},
                "title": {"type": "string", "minLength": 1},
                "category": {"type": "string", "minLength": 1},
                "description": {"type": "string", "minLength": 1},
                "qa_note": {"type": "string", "minLength": 1},
            },
            "additionalProperties": False,
        },
    ]
}

FORMAT_CHECKER = FormatChecker()


@pytest.fixture(scope="session")
def target_base_url() -> str:
    return os.getenv("AIQA_BASE_URL", "https://aiqa.su").rstrip("/")


@pytest.fixture
def course_session() -> str:
    return f"pytest-{uuid.uuid4()}"


@pytest.fixture
def http_lab_api(playwright, target_base_url, course_session):
    context = playwright.request.new_context(
        base_url=f"{target_base_url}/api/course/v1/http-lab/",
        extra_http_headers={"X-Course-Session": course_session},
    )
    yield context
    context.dispose()


@pytest.fixture
def create_api_user(http_lab_api):
    def _create_user(**overrides):
        payload = {
            "name": "QA Pytest",
            "email": f"qa-{uuid.uuid4()}@example.ru",
            "role": "viewer",
        }
        payload.update(overrides)
        response = request_json(http_lab_api, "POST", "users", payload)
        assert response.status == 201
        return response.json()

    return _create_user


@pytest.fixture
def new_http_lab_api_context(playwright, target_base_url):
    contexts = []

    def _new_context(*, session_header=None):
        headers = {}
        if session_header is not None:
            headers["X-Course-Session"] = session_header

        context = playwright.request.new_context(
            base_url=f"{target_base_url}/api/course/v1/http-lab/",
            extra_http_headers=headers or None,
        )
        contexts.append(context)
        return context

    yield _new_context

    for context in contexts:
        context.dispose()


@pytest.fixture
def lesson_page(page, target_base_url, course_session):
    allure.dynamic.parameter("session", course_session)
    with allure.step("Открыть страницу урока 4"):
        page.goto(f"{target_base_url}/base/lesson-4")
    with allure.step("Установить уникальную учебную сессию"):
        page.get_by_placeholder("student-demo").fill(course_session)
    return page


@pytest.fixture
def create_user_via_ui(lesson_page):
    def _create_user(name="UI Autotest", email=None, role="viewer"):
        email = email or f"ui-{uuid.uuid4()}@example.ru"
        with allure.step("Создать пользователя через форму"):
            lesson_page.get_by_label("name *").fill(name)
            lesson_page.get_by_label("email *").fill(email)
            lesson_page.get_by_label("role").select_option(role)
            with lesson_page.expect_response(
                lambda response: response.url.endswith("/api/course/v1/http-lab/users")
            ):
                lesson_page.get_by_role("button", name="POST /users").click()
        expect_response_status(lesson_page, 201)
        return {"name": name, "email": email, "role": role}

    return _create_user


def attach_screenshot(page, name):
    allure.attach(
        page.screenshot(full_page=True),
        name,
        allure.attachment_type.PNG,
    )


def expect_response_status(page, status_code: int):
    panel = page.get_by_text("Анатомия запроса и ответа").locator(
        "xpath=ancestor::div[contains(@class, 'rounded-xl')][1]"
    )
    with allure.step(f"Проверить статус {status_code} в панели запроса и ответа"):
        expect(panel).to_contain_text(f"{status_code}")
    return panel


def parse_iso_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def assert_payload_schema(payload: dict, schema: dict, *, schema_name: str):
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    assert not errors, f"{schema_name} schema validation failed: " + "; ".join(
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors
    )


def request_json(api_context, method: str, path: str, payload: dict):
    return api_context.fetch(
        path,
        method=method,
        data=json.dumps(payload, ensure_ascii=False),
        headers={"Content-Type": "application/json"},
    )


def assert_user_contract(user: dict, *, expected_id=None, expected_name=None, expected_email=None, expected_role=None):
    assert_payload_schema(user, USER_SCHEMA, schema_name="User")
    assert isinstance(user["id"], str) and user["id"]
    assert isinstance(user["name"], str) and user["name"]
    assert parse_iso_datetime(user["created_at"])
    assert parse_iso_datetime(user["updated_at"]) >= parse_iso_datetime(user["created_at"])

    if expected_id is not None:
        assert user["id"] == expected_id
    if expected_name is not None:
        assert user["name"] == expected_name
    if expected_email is not None:
        assert user["email"] == expected_email
    if expected_role is not None:
        assert user["role"] == expected_role


def assert_user_list_contract(body: dict, expected_session: str):
    assert_payload_schema(body, USER_LIST_SCHEMA, schema_name="UserListResponse")
    assert body["session"] == expected_session
    assert body["total"] == len(body["items"])

    seen_ids = set()
    for user in body["items"]:
        assert_user_contract(user)
        assert user["id"] not in seen_ids
        seen_ids.add(user["id"])


def assert_error_contract(body: dict):
    assert_payload_schema(body, ERROR_SCHEMA, schema_name="ErrorResponse")


def assert_status_code_contract(body: dict, *, expected_status_code: int):
    assert_payload_schema(body, STATUS_CODE_RESPONSE_SCHEMA, schema_name="StatusCodeResponse")
    returned_code = body.get("code", body.get("status"))
    returned_name = body.get("name", body.get("title"))
    assert returned_code == expected_status_code
    assert isinstance(returned_name, str) and returned_name
    assert body["category"].startswith(f"{expected_status_code // 100}")
    assert isinstance(body["description"], str) and body["description"]
    assert isinstance(body["qa_note"], str) and body["qa_note"]


def pytest_sessionfinish(session, exitstatus):
    allure_dir = Path(getattr(session.config.option, "allure_report_dir", None) or "allure-results")
    allure_dir.mkdir(parents=True, exist_ok=True)

    environment = {
        "Project": "AIQA lesson 4",
        "Base URL": os.getenv("AIQA_BASE_URL", "https://aiqa.su"),
        "Stack": "Python / pytest / Playwright",
        "Browser": "Chromium",
    }
    (allure_dir / "environment.properties").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()),
        encoding="utf-8",
    )

    categories = [
        {
            "name": "Assertion error",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*AssertionError.*",
        },
        {
            "name": "Browser or selector error",
            "matchedStatuses": ["broken"],
            "traceRegex": ".*(TimeoutError|Locator|strict mode|BrowserType).*",
        },
        {
            "name": "Network/API error",
            "matchedStatuses": ["failed", "broken"],
            "traceRegex": ".*(APIResponse|fetch|expect_response|Network).*",
        },
    ]
    (allure_dir / "categories.json").write_text(
        json.dumps(categories, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
