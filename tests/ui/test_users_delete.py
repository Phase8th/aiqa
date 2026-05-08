import allure
import pytest

from tests.conftest import UI_EPIC, UI_FEATURE, attach_screenshot, expect_response_status


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("DELETE /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("DELETE /users/{id} удаляет пользователя через UI")
@allure.description("Проверяем атомарное UI-действие DELETE и статус 204.")
def test_delete_user_displays_no_content(lesson_page, create_user_via_ui):
    create_user_via_ui(name="Delete UI User")

    with allure.step("Удалить пользователя через DELETE"):
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users/" in response.url):
            lesson_page.get_by_role("button", name="DELETE /users/{id}", exact=True).click()

    expect_response_status(lesson_page, 204)
    attach_screenshot(lesson_page, "DELETE user: 204")
