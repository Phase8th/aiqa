import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE, assert_error_contract, assert_user_contract, request_json


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Обновление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PUT /users/{id} полностью заменяет пользователя")
@allure.description("Проверяем, что PUT перезаписывает name, email и role.")
def test_put_user_replaces_all_fields(http_lab_api, create_api_user):
    with allure.step("Подготовить пользователя"):
        user = create_api_user(name="Before Put", email="before-put@example.ru", role="viewer")
        allure.dynamic.parameter("user_id", user["id"])

    payload = {"name": "After Put", "email": "after-put@example.ru", "role": "admin"}
    with allure.step("Отправить PUT /users/{id}"):
        response = request_json(http_lab_api, "PUT", f"users/{user['id']}", payload)

    with allure.step("Проверить статус 200 и замененные поля"):
        assert response.status == 200
        body = response.json()
        assert_user_contract(
            body,
            expected_id=user["id"],
            expected_name=payload["name"],
            expected_email=payload["email"],
            expected_role=payload["role"],
        )


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Обновление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PUT /users/{id} без role сбрасывает роль в значение по умолчанию")
@allure.description("Проверяем документированное поведение полного обновления без необязательного поля role.")
def test_put_user_without_role_resets_default_role(http_lab_api, create_api_user):
    with allure.step("Подготовить пользователя с ролью admin"):
        user = create_api_user(name="Before Put Default Role", role="admin")
        allure.dynamic.parameter("user_id", user["id"])

    payload = {"name": "After Put Default Role", "email": "after-default@example.ru"}
    with allure.step("Отправить PUT /users/{id} без role"):
        response = request_json(http_lab_api, "PUT", f"users/{user['id']}", payload)

    with allure.step("Проверить сброс role в viewer"):
        assert response.status == 200
        body = response.json()
        assert_user_contract(
            body,
            expected_id=user["id"],
            expected_name=payload["name"],
            expected_email=payload["email"],
            expected_role="viewer",
        )


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Обновление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PATCH /users/{id} изменяет только переданные поля")
@allure.description("Проверяем, что PATCH имени не меняет email и role.")
def test_patch_user_updates_only_name(http_lab_api, create_api_user):
    with allure.step("Подготовить пользователя"):
        user = create_api_user(name="Before Patch", email="before-patch@example.ru", role="editor")
        allure.dynamic.parameter("user_id", user["id"])

    with allure.step("Отправить PATCH /users/{id} только с name"):
        response = request_json(http_lab_api, "PATCH", f"users/{user['id']}", {"name": "After Patch"})

    with allure.step("Проверить статус 200 и частичное обновление"):
        assert response.status == 200
        body = response.json()
        assert_user_contract(
            body,
            expected_id=user["id"],
            expected_name="After Patch",
            expected_email="before-patch@example.ru",
            expected_role="editor",
        )


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Обновление пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PATCH /users/{id} возвращает 404 для несуществующего пользователя")
@allure.description("Проверяем ошибку частичного обновления по несуществующему id.")
def test_patch_missing_user_returns_404(http_lab_api):
    missing_id = "missing-user-id"
    allure.dynamic.parameter("user_id", missing_id)

    with allure.step("Отправить PATCH /users/{id} для несуществующего пользователя"):
        response = request_json(http_lab_api, "PATCH", f"users/{missing_id}", {"name": "No One"})

    with allure.step("Проверить статус 404 и сообщение об ошибке"):
        assert response.status == 404
        body = response.json()
        assert_error_contract(body)
        assert body["error"] == f"Пользователь {missing_id} не найден"
