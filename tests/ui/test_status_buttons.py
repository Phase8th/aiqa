import allure
import pytest
from playwright.sync_api import expect

from tests.conftest import UI_EPIC, UI_FEATURE, attach_locator_screenshot, expect_response_status
from tests.ui.locators import status_button


pytestmark = pytest.mark.ui


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("Кнопки статус-кодов")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Кнопка 422 показывает ошибку клиента")
@allure.description("Проверяем отдельную кнопку 422 в блоке статус-кодов.")
def test_422_status_button_displays_client_error(lesson_page):
    with allure.step("Нажать кнопку 422"):
        status_button(lesson_page, 422).click()

    panel = expect_response_status(lesson_page, 422)
    with allure.step("Проверить тело ответа 422"):
        expect(panel).to_contain_text('"category": "4xx')

    attach_locator_screenshot(panel, "Status button: 422")


@allure.epic(UI_EPIC)
@allure.feature(UI_FEATURE)
@allure.story("Кнопки статус-кодов")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Кнопка 204 показывает ответ без тела")
@allure.description("Проверяем отдельную кнопку 204 в блоке статус-кодов.")
def test_204_status_button_displays_empty_body(lesson_page):
    with allure.step("Нажать кнопку 204"):
        status_button(lesson_page, 204).click()

    panel = expect_response_status(lesson_page, 204)
    with allure.step("Проверить, что у 204 нет тела ответа"):
        expect(panel).not_to_contain_text('"status"')

    attach_locator_screenshot(panel, "Status button: 204 без тела")
