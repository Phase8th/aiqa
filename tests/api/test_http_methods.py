import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE


pytestmark = pytest.mark.api


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("HTTP-методы")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("HEAD /users возвращает 200 без тела ответа")
@allure.description("Проверяем учебную демонстрацию метода HEAD.")
def test_head_users_returns_no_body(http_lab_api):
    with allure.step("Отправить HEAD /users"):
        response = http_lab_api.head("users")

    with allure.step("Проверить статус 200 и пустое тело"):
        assert response.status == 200
        assert response.text() == ""


@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("HTTP-методы")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("OPTIONS /users возвращает 204 без тела ответа")
@allure.description("Проверяем учебную демонстрацию метода OPTIONS.")
def test_options_users_returns_no_body(http_lab_api):
    with allure.step("Отправить OPTIONS /users"):
        response = http_lab_api.fetch("users", method="OPTIONS")

    with allure.step("Проверить статус 204 и пустое тело"):
        assert response.status == 204
        assert response.text() == ""
