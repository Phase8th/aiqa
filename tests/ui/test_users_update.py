import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_screenshot, expect_response_status


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("PATCH /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PATCH /users/{id} изменяет имя пользователя через UI")
@allure.description("Проверяем атомарное UI-действие PATCH: меняется имя, email сохраняется.")
def test_patch_user_updates_name(lesson_page, create_user_via_ui):
    create_user_via_ui(name="Before Patch", email="before-patch@example.ru", role="viewer")

    with allure.step("Изменить имя пользователя через PATCH"):
        lesson_page.get_by_label("Новое имя для PATCH").fill("After Patch")
        with lesson_page.expect_response(lambda response: "/api/course/v1/http-lab/users/" in response.url):
            lesson_page.get_by_role("button", name="PATCH /users/{id}", exact=True).click()

    panel = expect_response_status(lesson_page, 200)
    with allure.step("Проверить, что изменилось только имя"):
        expect(panel).to_contain_text('"name": "After Patch"')
        expect(panel).to_contain_text('"email": "before-patch@example.ru"')
    attach_screenshot(lesson_page, "PATCH user: имя изменено")
