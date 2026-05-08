# AIQA autotests

## Setup

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run

```powershell
python -m pytest
```

Allure results are written to `allure-results` automatically. Generate the HTML report:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Optional target override:

```powershell
$env:AIQA_BASE_URL = "https://aiqa.su"
python -m pytest
```

Markers:

```powershell
python -m pytest -m api
python -m pytest -m ui
```

Test layout:

```text
tests/api/  API tests grouped by endpoint and action
tests/ui/   UI tests grouped by page flow
```

## GitLab CI

Pipeline is configured in `.gitlab-ci.yml`.

Stages:

```text
test    installs Python dependencies, installs Chromium, runs pytest
report  generates Allure HTML report from allure-results
pages   publishes Allure report on GitLab Pages for the default branch
```

Artifacts:

```text
allure-results/  raw Allure results from pytest
allure-report/   generated HTML report
junit.xml        GitLab test report
```

## GitHub Actions

Workflow is configured in `.github/workflows/tests.yml`.

It runs on:

```text
push to main
pull request
manual workflow_dispatch
```

Artifacts:

```text
allure-results/  raw Allure results
junit.xml        JUnit test report
```
