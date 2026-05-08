import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_screenshot, expect_response_status


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
            lesson_page.get_by_role("button", name="GET /users", exact=True).click()

    panel = expect_response_status(lesson_page, 200)
    with allure.step("Проверить детали запроса и ответа"):
        expect(panel).to_contain_text("GET")
        expect(panel).to_contain_text("/api/course/v1/http-lab/users")
        expect(panel).to_contain_text("X-Course-Session")
        expect(panel).to_contain_text(course_session)
        expect(panel).to_contain_text("user-001")
        expect(panel).to_contain_text('"total": 3')
    attach_screenshot(lesson_page, "GET users: панель ответа")


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("GET /users/{id}")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("GET /users/{id} показывает 404 после удаления пользователя")
@allure.description("Проверяем отдельный UI-сценарий получения удалённого пользователя.")
def test_get_deleted_user_displays_not_found(lesson_page, create_user_via_ui):
    create_user_via_ui(name="Deleted UI User")

    with allure.step("Удалить созданного пользователя"):
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users/" in response.url):
            lesson_page.get_by_role("button", name="DELETE /users/{id}", exact=True).click()
    expect_response_status(lesson_page, 204)

    with allure.step("Запросить удалённого пользователя через GET /users/{id}"):
        lesson_page.get_by_role("button", name="GET /users/{id}", exact=True).click()

    panel = expect_response_status(lesson_page, 404)
    with allure.step("Проверить текст ошибки 404"):
        expect(panel).to_contain_text("Пользователь")
        expect(panel).to_contain_text("не найден")
    attach_screenshot(lesson_page, "GET deleted user: 404")
