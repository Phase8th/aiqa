# AIQA autotests

Автотесты для тренажера HTTP из AIQA lesson 4.

Покрытие включает:

- API-тесты для `https://aiqa.su/api/course/v1/http-lab`
- UI-тесты для `https://aiqa.su/base/lesson-4`


## Стек

- Python 3.13
- pytest
- Playwright
- Allure
- jsonschema


## Установка

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
```


## Запуск

Все тесты:

```powershell
python -m pytest -q
```

Только API:

```powershell
python -m pytest -m api -q
```

Только UI:

```powershell
python -m pytest -m ui -q
```

Быстрый smoke-набор:

```powershell
python -m pytest tests/api/basic -q
```

Список собираемых тестов:

```powershell
python -m pytest --collect-only -q
```


## Переменные окружения

По умолчанию тесты идут в:

```text
https://aiqa.su
```

При необходимости можно переопределить target:

```powershell
$env:AIQA_BASE_URL = "https://aiqa.su"
python -m pytest -q
```


## Отчетность

Pytest автоматически пишет:

- `allure-results/`
- `junit.xml`

Локальная генерация HTML-отчета:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```


## Структура тестов

```text
tests/
  api/
    basic/                  быстрые API smoke-тесты
    test_http_methods.py
    test_status_codes.py
    test_users_create.py
    test_users_delete.py
    test_users_list.py
    test_users_read.py
    test_users_update.py
  ui/
    locators.py             общие UI-локаторы
    test_page_controls.py
    test_status_buttons.py
    test_users_create.py
    test_users_delete.py
    test_users_get.py
    test_users_update.py
  conftest.py               общие фикстуры, helper'ы, schema validation
```


## Что покрыто

### API

- `GET /users`
- `POST /users`
- `GET /users/{id}`
- `PUT /users/{id}`
- `PATCH /users/{id}`
- `DELETE /users/{id}`
- `HEAD /users`
- `OPTIONS /users`
- `GET /status/{code}`

Дополнительно проверяются:

- изоляция сессий
- дефолтные значения
- негативные сценарии
- контракт ответов через `jsonschema`


### UI

- стартовое состояние страницы тренажера
- создание пользователя
- получение списка пользователей
- получение удаленного пользователя
- обновление пользователя через PATCH
- удаление пользователя
- кнопки статус-кодов `422` и `204`


## Общая архитектура

Основная shared-логика находится в `tests/conftest.py`.

Там сосредоточены:

- API и UI фикстуры
- helper'ы подготовки данных
- schema validation
- helper'ы скриншотов
- helper'ы проверки response panel
- генерация Allure environment и categories


## CI/CD

В проекте используется несколько GitHub Actions workflow'ов.

### `pr-checks.yml`

Триггеры:

- `pull_request`
- `workflow_dispatch`

Что делает:

- ставит зависимости
- ставит Chromium
- запускает быстрый smoke-набор `tests/api/basic`
- сохраняет `pr-junit-report`


### `main-regression.yml`

Триггеры:

- `push` в `main`
- `workflow_dispatch`

Что делает:

- ставит зависимости
- ставит Chromium
- запускает полный `pytest -q`
- сохраняет:
  - `allure-results`
  - `junit-report`


### `publish-allure.yml`

Триггер:

- `workflow_run` после успешного `Main Regression`

Что делает:

- скачивает `allure-results`
- восстанавливает `history` из `gh-pages`
- генерирует `allure-report`
- публикует последний отчет в `gh-pages`
- архивирует каждый прогон в ветку `allure-report-history`


### `nightly-regression.yml`

Триггеры:

- ежедневный `schedule`
- `workflow_dispatch`

Что делает:

- запускает полный регресс
- сохраняет:
  - `nightly-allure-results`
  - `nightly-junit-report`


## GitLab CI

В репозитории также есть `.gitlab-ci.yml`.

Сценарий GitLab включает:

- запуск тестов
- генерацию Allure HTML report
- публикацию отчета через GitLab Pages


## Примечания

- Для UI-тестов локаторы централизованы в `tests/ui/locators.py`.
- Для API-тестов используется изоляция через `X-Course-Session`.
- Для `/status/{code}` в проекте учтен drift между документацией и фактическим ответом сервиса.
