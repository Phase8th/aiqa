import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE


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
        response = http_lab_api.put(f"users/{user['id']}", data=payload)

    with allure.step("Проверить статус 200 и заменённые поля"):
        assert response.status == 200
        body = response.json()
        assert body["id"] == user["id"]
        assert body["name"] == payload["name"]
        assert body["email"] == payload["email"]
        assert body["role"] == payload["role"]


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
        response = http_lab_api.patch(f"users/{user['id']}", data={"name": "After Patch"})

    with allure.step("Проверить статус 200 и частичное обновление"):
        assert response.status == 200
        body = response.json()
        assert body["id"] == user["id"]
        assert body["name"] == "After Patch"
        assert body["email"] == "before-patch@example.ru"
        assert body["role"] == "editor"
