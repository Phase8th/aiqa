import re

import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_screenshot, expect_response_status


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("POST /users")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("POST /users создаёт пользователя, подставляет id и включает CRUD-кнопки")
@allure.description(
    "Проверяем создание пользователя из формы и состояние кнопок GET/PUT/PATCH/DELETE после успешного POST."
)
def test_post_user_autofills_id_and_enables_crud_buttons(lesson_page):
    with allure.step("Заполнить форму создания пользователя"):
        lesson_page.get_by_label("name *").fill("UI Autotest")
        lesson_page.get_by_label("email *").fill("ui-autotest@example.ru")
        lesson_page.get_by_label("role").select_option("editor")

    with allure.step("Нажать POST /users"):
        with lesson_page.expect_response(lambda response: response.url.endswith("/api/course/v1/http-lab/users")):
            lesson_page.get_by_role("button", name="POST /users").click()

    panel = expect_response_status(lesson_page, 201)
    with allure.step("Проверить созданного пользователя и доступность кнопок"):
        expect(panel).to_contain_text('"name": "UI Autotest"')
        expect(panel).to_contain_text('"role": "editor"')

        user_id_input = lesson_page.get_by_label("id пользователя")
        expect(user_id_input).to_have_value(re.compile(r"[0-9a-f-]{36}"))
        expect(lesson_page.get_by_role("button", name="GET /users/{id}", exact=True)).to_be_enabled()
        expect(lesson_page.get_by_role("button", name="PUT /users/{id}", exact=True)).to_be_enabled()
        expect(lesson_page.get_by_role("button", name="DELETE /users/{id}", exact=True)).to_be_enabled()
        expect(lesson_page.get_by_role("button", name="PATCH /users/{id}", exact=True)).to_be_disabled()
    attach_screenshot(lesson_page, "POST users: пользователь создан")
