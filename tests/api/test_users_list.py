import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Список пользователей")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("GET /users возвращает 3 демо-пользователя для новой сессии")
@allure.description(
    "Проверяем стартовое состояние учебной сессии: API отдаёт список пользователей, "
    "корректный session id и ожидаемые demo id."
)
def test_get_users_returns_default_session_users(http_lab_api, course_session):
    allure.dynamic.parameter("session", course_session)

    with allure.step("Отправить GET /users"):
        response = http_lab_api.get("users")

    with allure.step("Проверить статус 200 и тело ответа"):
        assert response.status == 200
        body = response.json()
        allure.attach(str(body), "Ответ GET /users", allure.attachment_type.TEXT)
        assert body["session"] == course_session
        assert body["total"] == 3
        assert [user["id"] for user in body["items"]] == [
            "user-001",
            "user-002",
            "user-003",
        ]
