USER_NAME_LABEL = "name *"
USER_EMAIL_LABEL = "email *"
USER_ROLE_LABEL = "role"
USER_ID_LABEL = "id пользователя"
PATCH_NAME_LABEL = "Новое имя для PATCH"

TRAINER_HEADING = "Тренажёр HTTP-запросов"
SWAGGER_LINK = "Swagger документация API"

GET_USERS_BUTTON = "GET /users"
POST_USERS_BUTTON = "POST /users"
GET_USER_BY_ID_BUTTON = "GET /users/{id}"
PUT_USER_BUTTON = "PUT /users/{id}"
PATCH_USER_BUTTON = "PATCH /users/{id}"
DELETE_USER_BUTTON = "DELETE /users/{id}"


def method_button(page, name: str):
    return page.get_by_role("button", name=name, exact=True)


def status_button(page, code: int):
    return page.get_by_role("button", name=str(code))
