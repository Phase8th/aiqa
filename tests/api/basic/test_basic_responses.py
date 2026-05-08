import allure
import pytest

from tests.conftest import (
    API_EPIC,
    API_FEATURE,
    assert_user_contract,
    assert_user_list_contract,
    parse_iso_datetime,
)


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Базовые ответы API")
@allure.severity(allure.severity_level.MINOR)
@allure.title("GET /users возвращает JSON c корректным Content-Type")
@allure.description("Проверяем, что список пользователей приходит как JSON и соответствует базовому контракту.")
def test_get_users_returns_json_content_type(http_lab_api, course_session):
    with allure.step("Отправить GET /users"):
        response = http_lab_api.get("users")

    with allure.step("Проверить статус, Content-Type и тело ответа"):
        assert response.status == 200
        assert "application/json" in (response.headers.get("content-type") or "").lower()
        body = response.json()
        assert_user_list_contract(body, expected_session=course_session)


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Базовые ответы API")
@allure.severity(allure.severity_level.MINOR)
@allure.title("POST /users создает пользователя без истории изменений")
@allure.description("Проверяем, что сразу после создания updated_at совпадает с created_at.")
def test_create_user_has_same_created_and_updated_timestamps(create_api_user):
    with allure.step("Создать пользователя"):
        user = create_api_user(name="Timestamp User", email="timestamp-user@example.ru", role="viewer")

    with allure.step("Проверить контракт и стартовые timestamps"):
        assert_user_contract(
            user,
            expected_name="Timestamp User",
            expected_email="timestamp-user@example.ru",
            expected_role="viewer",
        )
        assert parse_iso_datetime(user["updated_at"]) == parse_iso_datetime(user["created_at"])
