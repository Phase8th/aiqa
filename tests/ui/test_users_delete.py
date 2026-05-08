import allure
import pytest

from tests.conftest import UI_EPIC, UI_FEATURE, attach_locator_screenshot, expect_response_status
from tests.ui.locators import DELETE_USER_BUTTON, method_button


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("DELETE /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("DELETE /users/{id} удаляет пользователя через UI")
@allure.description("Проверяем атомарное UI-действие DELETE и статус 204.")
def test_delete_user_displays_no_content(lesson_page, create_user_via_ui):
    create_user_via_ui(name="Delete UI User")

    with allure.step("Нажать DELETE /users/{id}"):
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users/" in response.url):
            method_button(lesson_page, DELETE_USER_BUTTON).click()

    panel = expect_response_status(lesson_page, 204)
    attach_locator_screenshot(panel, "DELETE user: 204")
