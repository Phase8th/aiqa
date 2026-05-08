import re

import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_screenshot
from tests.ui.locators import (
    DELETE_USER_BUTTON,
    GET_USER_BY_ID_BUTTON,
    GET_USERS_BUTTON,
    PATCH_USER_BUTTON,
    PUT_USER_BUTTON,
    SWAGGER_LINK,
    TRAINER_HEADING,
    method_button,
)


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("Стартовое состояние страницы")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("На странице урока доступны основные элементы тренажера")
@allure.description(
    "Проверяем заголовок, ссылку на Swagger и состояние кнопок до выбора id пользователя."
)
def test_lesson_page_has_main_controls(lesson_page):
    with allure.step("Проверить стартовое состояние интерфейса"):
        expect(lesson_page).to_have_title(re.compile("Тренажёр HTTP"))
        expect(lesson_page.get_by_role("heading", name=TRAINER_HEADING)).to_be_visible()
        expect(lesson_page.get_by_role("link", name=SWAGGER_LINK)).to_have_attribute(
            "href", "/base/lesson-4/docs"
        )
        expect(method_button(lesson_page, GET_USERS_BUTTON)).to_be_enabled()
        expect(method_button(lesson_page, GET_USER_BY_ID_BUTTON)).to_be_disabled()
        expect(method_button(lesson_page, PUT_USER_BUTTON)).to_be_disabled()
        expect(method_button(lesson_page, PATCH_USER_BUTTON)).to_be_disabled()
        expect(method_button(lesson_page, DELETE_USER_BUTTON)).to_be_disabled()

    attach_screenshot(lesson_page, "Стартовое состояние страницы")
