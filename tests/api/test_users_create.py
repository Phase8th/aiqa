import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE, assert_user_contract, request_json


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
        response = request_json(http_lab_api, "POST", "users", payload)

    with allure.step("Проверить статус 201 и поля созданного пользователя"):
        assert response.status == 201
        body = response.json()
        allure.dynamic.parameter("created_user_id", body["id"])
        allure.attach(str(body), "Созданный пользователь", allure.attachment_type.TEXT)
        assert_user_contract(
            body,
            expected_name=payload["name"],
            expected_email=payload["email"],
            expected_role=payload["role"],
        )


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Создание пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("POST /users добавляет пользователя в GET /users текущей сессии")
@allure.description("Проверяем, что после создания пользователь виден в списке и total увеличивается.")
def test_create_user_is_visible_in_list(http_lab_api):
    payload = {"name": "Visible User", "email": "visible-user@example.ru", "role": "editor"}

    with allure.step("Получить стартовый список пользователей"):
        initial_response = http_lab_api.get("users")
        assert initial_response.status == 200
        initial_body = initial_response.json()

    with allure.step("Создать пользователя"):
        create_response = request_json(http_lab_api, "POST", "users", payload)
        assert create_response.status == 201
        created_user = create_response.json()

    with allure.step("Повторно получить список пользователей"):
        list_response = http_lab_api.get("users")

    with allure.step("Проверить, что список содержит созданного пользователя"):
        assert list_response.status == 200
        list_body = list_response.json()
        assert list_body["total"] == initial_body["total"] + 1
        assert created_user["id"] in {user["id"] for user in list_body["items"]}


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Создание пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("POST /users без role создает пользователя с ролью по умолчанию")
@allure.description("Проверяем, что необязательное поле role заполняется значением по умолчанию.")
def test_create_user_without_role_uses_default_role(http_lab_api):
    payload = {"name": "Default Role", "email": "default-role@example.ru"}

    with allure.step("Отправить POST /users без role"):
        response = request_json(http_lab_api, "POST", "users", payload)

    with allure.step("Проверить статус 201 и роль по умолчанию"):
        assert response.status == 201
        body = response.json()
        assert_user_contract(
            body,
            expected_name=payload["name"],
            expected_email=payload["email"],
            expected_role="viewer",
        )


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
        pytest.param(
            "Некорректный email",
            {"name": "Bad Email", "email": "not-an-email", "role": "viewer"},
            None,
            id="invalid-email",
        ),
        pytest.param(
            "Некорректная роль",
            {"name": "Bad Role", "email": "bad-role@example.ru", "role": "owner"},
            None,
            id="invalid-role",
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
        response = request_json(http_lab_api, "POST", "users", payload)

    with allure.step("Проверить статус 422 и сообщение об ошибке"):
        assert response.status == 422
        body = response.json()
        assert isinstance(body["error"], str) and body["error"]
        if expected_error is not None:
            assert body["error"] == expected_error
