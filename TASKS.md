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

- [ ] Triggers: `push` and `pull_request`
- [ ] Steps: checkout → setup Python 3.11 → install uv → `uv sync` → run Ruff → run pytest
- [ ] Workflow fails if Ruff or pytest fails

## 5. Deploy — `.github/workflows/deploy.yml`

- [ ] Trigger: `push` to `main` only
- [ ] Runs only if CI succeeds (gate on CI, e.g. `workflow_run` or job dependency)
- [ ] Azure Login via OIDC (no publish profile)
- [ ] Placeholder env/secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_WEBAPP_NAME`
- [ ] Placeholder steps: checkout → setup Python → install uv → build app → Azure Login (placeholder) → deploy to Azure Web App (placeholder)
- [ ] All Azure-specific values left empty with clear `TODO` comments

## 6. Documentation — `README.md`

- [ ] uv installation instructions
- [ ] `uv sync`
- [ ] Running locally (`uv run uvicorn app.main:app --reload`)
- [ ] Running tests (`pytest`)
- [ ] Running Ruff
- [ ] Environment variables
- [ ] GitHub Actions overview
- [ ] Azure deployment placeholders

## 7. Final verification (Acceptance Criteria)

- [ ] App runs with `uv run uvicorn app.main:app --reload`
- [ ] `GET /health` returns healthy
- [ ] `POST /chat` returns the LangChain service response
- [ ] LangChain service is isolated from FastAPI
- [ ] All tests pass
- [ ] Ruff passes
- [ ] CI runs automatically on every push and pull request
- [ ] Every push to `main` triggers the deployment workflow
- [ ] Deployment workflow is production-ready except Azure placeholders
- [ ] Structure is clean, minimal, and easy to extend with OpenAI/RAG later
