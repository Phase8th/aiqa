import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Создание пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("POST /users создаёт пользователя")
@allure.description("Проверяем успешное создание пользователя через API.")
def test_create_user_returns_created_user(http_lab_api):
    payload = {"name": "QA Pytest", "email": "qa-pytest@example.ru", "role": "viewer"}

    with allure.step("Отправить POST /users"):
        response = http_lab_api.post("users", data=payload)

    with allure.step("Проверить статус 201 и поля созданного пользователя"):
        assert response.status == 201
        body = response.json()
        allure.dynamic.parameter("created_user_id", body["id"])
        allure.attach(str(body), "Созданный пользователь", allure.attachment_type.TEXT)
        assert body["name"] == payload["name"]
        assert body["email"] == payload["email"]
        assert body["role"] == payload["role"]


@pytest.mark.parametrize(
    ("case_name", "payload", "expected_error"),
    [
        pytest.param(
            "Пустое имя",
            {"name": "", "email": "empty-name@example.ru", "role": "viewer"},
            "name обязателен",
            id="empty-name",
        ),
        pytest.param(
            "Пустой email",
            {"name": "No Email", "email": "", "role": "viewer"},
            "email обязателен",
            id="empty-email",
        ),
    ],
)
@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Валидация создания пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("POST /users отклоняет некорректные данные: {case_name}")
@allure.description("Проверяем, что API возвращает 422 и понятное сообщение об ошибке валидации.")
def test_create_user_validation_errors(http_lab_api, case_name, payload, expected_error):
    allure.dynamic.parameter("Проверка", case_name)

    with allure.step("Отправить некорректный POST /users"):
        response = http_lab_api.post("users", data=payload)

    with allure.step("Проверить статус 422 и текст ошибки"):
        assert response.status == 422
        assert response.json()["error"] == expected_error
