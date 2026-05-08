import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_locator_screenshot, expect_response_status
from tests.ui.locators import DELETE_USER_BUTTON, GET_USER_BY_ID_BUTTON, GET_USERS_BUTTON, method_button


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("GET /users")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Кнопка GET /users показывает анатомию запроса и ответа")
@allure.description(
    "Проверяем, что тренажёр отправляет GET /users и показывает метод, URL, X-Course-Session и JSON-ответ."
)
def test_get_users_displays_request_and_response(lesson_page, course_session):
    with allure.step("Нажать GET /users"):
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users" in response.url):
            method_button(lesson_page, GET_USERS_BUTTON).click()

    panel = expect_response_status(lesson_page, 200)
    with allure.step("Проверить детали запроса и ответа"):
        expect(panel).to_contain_text("GET")
        expect(panel).to_contain_text("/api/course/v1/http-lab/users")
        expect(panel).to_contain_text("X-Course-Session")
        expect(panel).to_contain_text(course_session)
        expect(panel).to_contain_text("user-001")
        expect(panel).to_contain_text('"total": 3')

    attach_locator_screenshot(panel, "GET users: панель ответа")


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("GET /users/{id}")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("GET /users/{id} показывает 404 после удаления пользователя")
@allure.description("Проверяем отдельный UI-сценарий получения удалённого пользователя.")
def test_get_deleted_user_displays_not_found(lesson_page, create_user_via_ui):
    create_user_via_ui(name="Deleted UI User")

    with allure.step("Нажать DELETE /users/{id}"):
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users/" in response.url):
            method_button(lesson_page, DELETE_USER_BUTTON).click()
    expect_response_status(lesson_page, 204)

    with allure.step("Нажать GET /users/{id}"):
        method_button(lesson_page, GET_USER_BY_ID_BUTTON).click()

    panel = expect_response_status(lesson_page, 404)
    with allure.step("Проверить текст ошибки 404"):
        expect(panel).to_contain_text("Пользователь")
        expect(panel).to_contain_text("не найден")

    attach_locator_screenshot(panel, "GET deleted user: 404")
