import re

import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_screenshot


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("Стартовое состояние страницы")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("На странице урока доступны основные элементы тренажёра")
@allure.description(
    "Проверяем заголовок, ссылку на Swagger и состояние кнопок до выбора id пользователя."
)
def test_lesson_page_has_main_controls(lesson_page):
    with allure.step("Проверить стартовое состояние интерфейса"):
        expect(lesson_page).to_have_title(re.compile("Тренажёр HTTP"))
        expect(lesson_page.get_by_role("heading", name="Тренажёр HTTP-запросов")).to_be_visible()
        expect(lesson_page.get_by_role("link", name="Swagger документация API")).to_have_attribute(
            "href", "/base/lesson-4/docs"
        )
        expect(lesson_page.get_by_role("button", name="GET /users", exact=True)).to_be_enabled()
        expect(lesson_page.get_by_role("button", name="GET /users/{id}", exact=True)).to_be_disabled()
        expect(lesson_page.get_by_role("button", name="PUT /users/{id}", exact=True)).to_be_disabled()
        expect(lesson_page.get_by_role("button", name="PATCH /users/{id}", exact=True)).to_be_disabled()
        expect(lesson_page.get_by_role("button", name="DELETE /users/{id}", exact=True)).to_be_disabled()
    attach_screenshot(lesson_page, "Стартовое состояние страницы")
