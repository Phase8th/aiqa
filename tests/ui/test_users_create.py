import re

import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_locator_screenshot, expect_response_status
from tests.ui.locators import (
    DELETE_USER_BUTTON,
    GET_USER_BY_ID_BUTTON,
    PATCH_USER_BUTTON,
    POST_USERS_BUTTON,
    PUT_USER_BUTTON,
    USER_EMAIL_LABEL,
    USER_ID_LABEL,
    USER_NAME_LABEL,
    USER_ROLE_LABEL,
    method_button,
)


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
    with allure.step("Ввести данные пользователя"):
        lesson_page.get_by_label(USER_NAME_LABEL).fill("UI Autotest")
        lesson_page.get_by_label(USER_EMAIL_LABEL).fill("ui-autotest@example.ru")
        lesson_page.get_by_label(USER_ROLE_LABEL).select_option("editor")

    with allure.step("Нажать POST /users"):
        with lesson_page.expect_response(lambda response: response.url.endswith("/api/course/v1/http-lab/users")):
            method_button(lesson_page, POST_USERS_BUTTON).click()

    panel = expect_response_status(lesson_page, 201)
    with allure.step("Проверить созданного пользователя и состояние кнопок"):
        expect(panel).to_contain_text('"name": "UI Autotest"')
        expect(panel).to_contain_text('"role": "editor"')

        user_id_input = lesson_page.get_by_label(USER_ID_LABEL)
        expect(user_id_input).to_have_value(re.compile(r"[0-9a-f-]{36}"))
        expect(method_button(lesson_page, GET_USER_BY_ID_BUTTON)).to_be_enabled()
        expect(method_button(lesson_page, PUT_USER_BUTTON)).to_be_enabled()
        expect(method_button(lesson_page, DELETE_USER_BUTTON)).to_be_enabled()
        expect(method_button(lesson_page, PATCH_USER_BUTTON)).to_be_disabled()

    attach_locator_screenshot(panel, "POST users: пользователь создан")
