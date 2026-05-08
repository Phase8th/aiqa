import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE, assert_user_list_contract


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
        assert_user_list_contract(body, expected_session=course_session)
        assert body["total"] == 3
        assert [user["id"] for user in body["items"]] == [
            "user-001",
            "user-002",
            "user-003",
        ]


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Изоляция сессий")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("POST /users создает пользователя только в рамках текущей сессии")
@allure.description("Проверяем, что данные одной учебной сессии не видны в другой.")
def test_user_created_in_one_session_is_not_visible_in_another(
    create_api_user,
    new_http_lab_api_context,
):
    with allure.step("Создать пользователя в первой сессии"):
        created_user = create_api_user(name="Isolated User")
        allure.dynamic.parameter("user_id", created_user["id"])

    second_context = new_http_lab_api_context(session_header="pytest-isolated-second-session")

    with allure.step("Запросить список пользователей из другой сессии"):
        response = second_context.get("users")

    with allure.step("Проверить, что созданного пользователя нет во второй сессии"):
        assert response.status == 200
        body = response.json()
        assert body["session"] == "pytest-isolated-second-session"
        assert created_user["id"] not in {user["id"] for user in body["items"]}


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Сессии и cookie")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("GET /users без X-Course-Session создает cookie-сессию и сохраняет ее в контексте")
@allure.description("Проверяем документированное поведение API без session header.")
def test_get_users_without_session_header_uses_cookie_session(new_http_lab_api_context):
    api_context = new_http_lab_api_context()

    with allure.step("Отправить два GET /users в одном контексте без X-Course-Session"):
        first_response = api_context.get("users")
        second_response = api_context.get("users")

    with allure.step("Проверить, что API использует одну и ту же cookie-сессию"):
        assert first_response.status == 200
        assert second_response.status == 200
        first_body = first_response.json()
        second_body = second_response.json()
        assert_user_list_contract(first_body, expected_session=first_body["session"])
        assert_user_list_contract(second_body, expected_session=first_body["session"])
        assert first_body["session"]
