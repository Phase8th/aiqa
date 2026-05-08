import allure
import pytest

from tests.conftest import API_EPIC, API_FEATURE


pytestmark = pytest.mark.api


@pytest.mark.parametrize(
    "status_code",
    [
        pytest.param(200, id="200 OK"),
        pytest.param(201, id="201 Created"),
        pytest.param(204, id="204 No Content"),
        pytest.param(301, id="301 Moved Permanently"),
        pytest.param(302, id="302 Found"),
        pytest.param(400, id="400 Bad Request"),
        pytest.param(401, id="401 Unauthorized"),
        pytest.param(403, id="403 Forbidden"),
        pytest.param(404, id="404 Not Found"),
        pytest.param(422, id="422 Unprocessable Entity"),
        pytest.param(500, id="500 Internal Server Error"),
        pytest.param(503, id="503 Service Unavailable"),
    ],
)
@allure.epic(API_EPIC)
@allure.feature(API_FEATURE)
@allure.story("Справочник статус-кодов")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("GET /status/{status_code} возвращает HTTP {status_code}")
@allure.description("Проверяем, что учебный endpoint возвращает именно тот статус-код, который указан в URL.")
def test_status_endpoint_returns_requested_code(http_lab_api, status_code):
    with allure.step(f"Отправить GET /status/{status_code}"):
        response = http_lab_api.get(f"status/{status_code}", max_redirects=0)

    with allure.step("Проверить код ответа и тело"):
        assert response.status == status_code
        if status_code == 204:
            assert response.text() == ""
        else:
            body = response.json()
            allure.attach(str(body), f"Ответ /status/{status_code}", allure.attachment_type.TEXT)
            assert set(body) >= {"description", "qa_note", "category"}
            returned_code = body.get("code", body.get("status"))
            returned_name = body.get("name", body.get("title"))
            assert returned_code == status_code
            assert isinstance(returned_name, str) and returned_name
            assert body["category"].startswith(f"{status_code // 100}")
            assert isinstance(body["description"], str) and body["description"]
            assert isinstance(body["qa_note"], str) and body["qa_note"]
