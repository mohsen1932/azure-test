# azure-test

A small but production-style **FastAPI** application demonstrating clean
architecture and a complete CI/CD pipeline.

The app is intentionally simple: it exposes a health check and a `/chat`
endpoint that delegates to a `LangChainService`. The service currently returns
a static string — there is **no OpenAI, RAG, embeddings, or vector database
yet**. The structure is designed so those can be added later without touching
the API layer.

## Project layout

```text
app/
  main.py                     # FastAPI app + router wiring
  config.py                   # pydantic-settings configuration
  dependencies.py             # dependency-injection providers
  api/routes.py               # GET /health, POST /chat (delegate to service)
  services/langchain_service.py  # LangChainService (static response for now)
tests/                        # pytest suite (fully async httpx client)
.github/workflows/            # ci.yml, deploy.yml
```

## Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/)

## Installing uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew
brew install uv

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/)
for other methods.

## Setup

Install dependencies (creates the virtual environment and uses the committed
lockfile):

```bash
uv sync
```

## Running locally

```bash
uv run uvicorn app.main:app --reload
```

The API is then available at http://127.0.0.1:8000 (interactive docs at
http://127.0.0.1:8000/docs).

### Endpoints

```bash
# Health check
curl http://127.0.0.1:8000/health
# {"status":"healthy"}

# Chat
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
# {"response":"Hello from LangChain service!"}
```

## Running tests

```bash
uv run pytest
```

## Running Ruff

```bash
uv run ruff check .      # lint
uv run ruff format .     # auto-format
```

## Environment variables

Copy the example file and fill in values as needed:

```bash
cp .env.example .env
```

| Variable         | Default         | Notes                                    |
| ---------------- | --------------- | ---------------------------------------- |
| `OPENAI_API_KEY` | _(empty)_       | Defined for the future; **not used yet** |
| `OPENAI_MODEL`   | `gpt-4.1-mini`  | Defined for the future; **not used yet** |

Configuration is loaded via `pydantic-settings` (`app/config.py`) from the
environment and an optional `.env` file. `.env` is git-ignored.

## GitHub Actions

### CI — `.github/workflows/ci.yml`

Runs on every `push` and `pull_request`:

1. Checkout
2. Set up Python 3.11
3. Install uv
4. `uv sync --locked`
5. `ruff check .`
6. `pytest`

The workflow fails if linting or tests fail.

### Deploy — `.github/workflows/deploy.yml`

Runs on every `push` to `main`. A `verify` job re-runs the lint + test checks,
and the `deploy` job uses `needs: verify` so **deployment only runs if the
checks succeed**. Authentication uses **Azure Login via OIDC** (no publish
profile).

The deploy target is a **code-based Azure App Service on the free F1 tier**
(no Docker). Because App Service's Oryx build does not understand uv, the
deploy job exports a `requirements.txt` from `uv.lock`
(`uv export --frozen --no-dev`) so Oryx's `pip install` is reproducible. The
app is started with:

```text
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Azure deployment placeholders

The deploy workflow is production-ready except for Azure-specific values, which
are intentionally left as placeholders marked with `TODO`. Before deploying,
create the following as GitHub Actions **secrets** (Settings → Secrets and
variables → Actions) and fill in the workflow env values:

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_WEBAPP_NAME`

You will also need to configure a federated credential on the Azure AD app
registration so GitHub's OIDC token is trusted for this repository. Until these
are set, the deploy job's Azure steps are placeholders and will not perform a
real deployment.

On the Azure side (one-time), for the free F1 code-based deploy:

- Create a **Linux, Python 3.11** App Service Web App on a **Free (F1)** plan.
- Set the app setting **`SCM_DO_BUILD_DURING_DEPLOYMENT=true`** so Oryx runs
  `pip install -r requirements.txt` on deploy.
- The startup command is provided by the workflow (see above); it can also be
  set on the Web App's **Configuration → Startup Command**.
