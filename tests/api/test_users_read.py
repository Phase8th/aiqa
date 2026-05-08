import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE, assert_error_contract, assert_user_contract


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Получение пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("GET /users/{id} возвращает существующего пользователя")
@allure.description("Проверяем чтение одного пользователя по id.")
def test_get_user_by_id_returns_created_user(http_lab_api, create_api_user):
    with allure.step("Подготовить пользователя"):
        user = create_api_user(name="Read User", role="editor")
        allure.dynamic.parameter("user_id", user["id"])

    with allure.step("Отправить GET /users/{id}"):
        response = http_lab_api.get(f"users/{user['id']}")

    with allure.step("Проверить статус 200 и данные пользователя"):
        assert response.status == 200
        body = response.json()
        assert_user_contract(
            body,
            expected_id=user["id"],
            expected_name="Read User",
            expected_email=user["email"],
            expected_role="editor",
        )


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Получение пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("GET /users/{id} возвращает 404 для несуществующего пользователя")
@allure.description("Проверяем ошибку чтения пользователя, которого нет в сессии.")
def test_get_missing_user_returns_404(http_lab_api):
    missing_id = "missing-user-id"
    allure.dynamic.parameter("user_id", missing_id)

    with allure.step("Отправить GET /users/{id} с несуществующим id"):
        response = http_lab_api.get(f"users/{missing_id}")

    with allure.step("Проверить статус 404 и текст ошибки"):
        assert response.status == 404
        body = response.json()
        assert_error_contract(body)
        assert body["error"] == f"Пользователь {missing_id} не найден"
