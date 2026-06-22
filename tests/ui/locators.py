USER_NAME_LABEL = "name *"
USER_EMAIL_LABEL = "email *"
USER_ROLE_LABEL = "role"
USER_ID_LABEL = "id пользователя (для GET/PUT/PATCH/DELETE одного)"
PATCH_NAME_LABEL = "Новое имя для PATCH (остальные поля не изменятся)"

GET_SECTION_MARKER = "01GET"
POST_SECTION_MARKER = "02POST"
PUT_PATCH_SECTION_MARKER = "03PUT и PATCH"

TRAINER_HEADING = "Тренажёр HTTP-запросов"
SWAGGER_LINK = "Swagger документация API"

GET_USERS_BUTTON = "GET /users"
POST_USERS_BUTTON = "POST /users"
GET_USER_BY_ID_BUTTON = "GET /users/{id}"
PUT_USER_BUTTON = "PUT /users/{id}"
PATCH_USER_BUTTON = "PATCH /users/{id}"
DELETE_USER_BUTTON = "DELETE /users/{id}"


def get_section(page):
    return page.locator("section").filter(has_text=GET_SECTION_MARKER)


def post_section(page):
    return page.locator("section").filter(has_text=POST_SECTION_MARKER)


def put_patch_section(page):
    return page.locator("section").filter(has_text=PUT_PATCH_SECTION_MARKER)


def method_button(page, name: str):
    return page.get_by_role("button", name=name, exact=True)


def status_button(page, code: int):
    return page.get_by_role("button", name=str(code))
