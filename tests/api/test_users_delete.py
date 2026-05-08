import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Удаление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("DELETE /users/{id} удаляет пользователя и возвращает 204")
@allure.description("Проверяем атомарно действие удаления пользователя.")
def test_delete_user_returns_no_content(http_lab_api, create_api_user):
    with allure.step("Подготовить пользователя"):
        user = create_api_user(name="Delete User")
        allure.dynamic.parameter("user_id", user["id"])

    with allure.step("Отправить DELETE /users/{id}"):
        response = http_lab_api.delete(f"users/{user['id']}")

    with allure.step("Проверить статус 204 и пустое тело"):
        assert response.status == 204
        assert response.text() == ""


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Удаление пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("GET /users/{id} после DELETE возвращает 404")
@allure.description("Проверяем эффект удаления отдельным коротким сценарием.")
def test_deleted_user_is_not_available(http_lab_api, create_api_user):
    with allure.step("Подготовить и удалить пользователя"):
        user = create_api_user(name="Deleted User")
        allure.dynamic.parameter("user_id", user["id"])
        delete_response = http_lab_api.delete(f"users/{user['id']}")
        assert delete_response.status == 204

    with allure.step("Отправить GET /users/{id} после удаления"):
        response = http_lab_api.get(f"users/{user['id']}")

    with allure.step("Проверить статус 404"):
        assert response.status == 404
        assert response.json()["error"] == f"Пользователь {user['id']} не найден"
