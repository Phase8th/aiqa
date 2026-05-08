import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_locator_screenshot, expect_response_status
from tests.ui.locators import PATCH_NAME_LABEL, PATCH_USER_BUTTON, method_button


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("PATCH /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PATCH /users/{id} изменяет имя пользователя через UI")
@allure.description("Проверяем атомарное UI-действие PATCH: меняется имя, email сохраняется.")
def test_patch_user_updates_name(lesson_page, create_user_via_ui):
    create_user_via_ui(name="Before Patch", email="before-patch@example.ru", role="viewer")

    with allure.step("Ввести новое имя для PATCH"):
        lesson_page.get_by_label(PATCH_NAME_LABEL).fill("After Patch")

    with allure.step("Нажать PATCH /users/{id}"):
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users/" in response.url):
            method_button(lesson_page, PATCH_USER_BUTTON).click()

    panel = expect_response_status(lesson_page, 200)
    with allure.step("Проверить, что изменилось только имя"):
        expect(panel).to_contain_text('"name": "After Patch"')
        expect(panel).to_contain_text('"email": "before-patch@example.ru"')

    attach_locator_screenshot(panel, "PATCH user: имя изменено")
