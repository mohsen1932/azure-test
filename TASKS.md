# TASKS.md

Task breakdown for the FastAPI + LangChain-stub + CI/CD project defined in [PROJECT.md](./PROJECT.md).

Mark a task done by changing `[ ]` to `[x]`.

---

## 1. Project scaffolding & tooling

- [x] Create `pyproject.toml` (Python 3.11, project metadata, dependencies: fastapi, langchain, pydantic v2, pydantic-settings, uvicorn; dev deps: pytest, ruff, httpx for the test client)
- [x] Configure `uv` (ensure `uv sync` works, lockfile generated)
- [x] Configure Ruff in `pyproject.toml` (lint + format rules, target py311)
- [x] Create `.gitignore` (Python, venv, `.env`, caches, IDE files)
- [x] Create `.env.example` with `OPENAI_API_KEY=` and `OPENAI_MODEL=gpt-4.1-mini` (defined but unused)

## 2. Application code (`app/`)

- [x] `app/__init__.py` (package marker)
- [x] `app/config.py` — `Settings` using pydantic-settings, loads env vars (openai key/model, kept but unused)
- [x] `app/services/__init__.py`
- [x] `app/services/langchain_service.py` — `LangChainService` class with `async def invoke(self, message: str) -> str` returning the static string
- [x] `app/dependencies.py` — dependency-injection providers (e.g. `get_langchain_service`, `get_settings`)
- [x] `app/api/__init__.py`
- [x] `app/api/routes.py` — `GET /health` and `POST /chat`; routes only delegate to the service, no business logic
- [x] Pydantic v2 request/response models for `/chat` (`ChatRequest`, `ChatResponse`)
- [x] `app/main.py` — create FastAPI app, include router

## 3. Tests (`tests/`)

- [x] `tests/__init__.py`
- [x] `tests/test_health.py` — assert `GET /health` returns `{"status": "healthy"}`
- [x] `tests/test_chat.py` — assert `POST /chat` with `{"message": "Hello"}` returns `{"response": "Hello from LangChain service!"}`
- [x] `tests/test_langchain_service.py` — unit test the service in isolation
- [x] `tests/conftest.py` — async httpx client fixture (pytest-asyncio)
- [x] Ensure all tests pass with `pytest`

## 4. CI — `.github/workflows/ci.yml`

- [x] Triggers: `push` and `pull_request`
- [x] Steps: checkout → setup Python 3.11 → install uv → `uv sync` → run Ruff → run pytest
- [x] Workflow fails if Ruff or pytest fails

## 5. Deploy — `.github/workflows/deploy.yml`

- [x] Trigger: `push` to `main` only
- [x] Runs only if CI succeeds (gate on CI, e.g. `workflow_run` or job dependency)
- [x] Azure Login via OIDC (no publish profile)
- [x] Placeholder env/secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_WEBAPP_NAME`
- [x] Placeholder steps: checkout → setup Python → install uv → build app → Azure Login (placeholder) → deploy to Azure Web App (placeholder)
- [x] All Azure-specific values left empty with clear `TODO` comments
- [x] Free F1 (code-based) target: export `requirements.txt` from `uv.lock` for Oryx, set uvicorn startup command, document `SCM_DO_BUILD_DURING_DEPLOYMENT` (test in `tests/test_requirements_export.py`)

## 6. Documentation — `README.md`

- [x] uv installation instructions
- [x] `uv sync`
- [x] Running locally (`uv run uvicorn app.main:app --reload`)
- [x] Running tests (`pytest`)
- [x] Running Ruff
- [x] Environment variables
- [x] GitHub Actions overview
- [x] Azure deployment placeholders

## 7. Final verification (Acceptance Criteria)

- [x] App runs with `uv run uvicorn app.main:app --reload`
- [x] `GET /health` returns healthy
- [x] `POST /chat` returns the LangChain service response
- [x] LangChain service is isolated from FastAPI
- [x] All tests pass
- [x] Ruff passes
- [x] CI runs automatically on every push and pull request
- [x] Every push to `main` triggers the deployment workflow
- [x] Deployment workflow is production-ready except Azure placeholders
- [x] Structure is clean, minimal, and easy to extend with OpenAI/RAG later

---

## 8. Azure provisioning & OIDC integration (make CI/CD work end to end)

Prereqs: az CLI installed and logged in (`az login` done); `gh` CLI available
and authenticated for setting GitHub secrets (or set them in the GitHub UI).

### 8a. Provision the App Service (free F1)

- [x] Decide/record names: RG `azure-test-rg`, plan `azure-test-plan`, app `azure-test-mohsen1932`, region `francecentral` (only region with F1 quota)
- [x] Create resource group
- [x] Create Linux App Service plan on the **Free (F1)** SKU
- [x] Create the Web App with the **Python 3.11** runtime on that plan
- [x] Set app setting `SCM_DO_BUILD_DURING_DEPLOYMENT=true` (Oryx builds from requirements.txt)
- [x] Set the startup command (`python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`)

### 8b. Set up OIDC (federated identity, no secrets/publish profile)

- [x] Create an Azure AD app registration (+ service principal) for GitHub Actions
- [x] Assign it an RBAC role (Contributor) scoped to the resource group
- [x] Add a federated credential for `repo:mohsen1932/azure-test:ref:refs/heads/main`
- [x] Collect `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`

### 8c. Wire up GitHub

- [x] Set repo secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`
- [x] Put the real web app name into `deploy.yml` (`AZURE_WEBAPP_NAME`, non-secret) and commit
- [x] Push to `main` to trigger CI → deploy
- [x] Fix federated credential subject to GitHub's immutable form (`repo:mohsen1932@3251348/azure-test@1308020905:ref:refs/heads/main`)

### 8d. End-to-end verification

- [x] CI workflow passes
- [x] Deploy workflow `verify` + `deploy` jobs both succeed
- [x] Live `GET /health` on the Azure URL returns `{"status":"healthy"}`
- [x] Live `POST /chat` on the Azure URL returns the service response
