# PROJECT.md

# Objective

Build a **small but production-style FastAPI application** that
demonstrates a clean architecture and a complete CI/CD pipeline.

The application should be intentionally simple while following
production engineering practices.

The application **does not use OpenAI yet**.

The LangChain service simply returns a static string.

The Azure deployment configuration must be fully prepared but contain
**only placeholders** for Azure-specific values.

------------------------------------------------------------------------

# Technology Stack

-   Python 3.11
-   FastAPI
-   uv
-   LangChain
-   Pydantic v2
-   pydantic-settings
-   pytest
-   Ruff
-   GitHub Actions

------------------------------------------------------------------------

# Architecture

``` text
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   └── services/
│       └── langchain_service.py
│
├── tests/
│   ├── test_health.py
│   └── test_chat.py
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── .env.example
├── pyproject.toml
├── README.md
└── .gitignore
```

------------------------------------------------------------------------

# API

## GET /health

Returns

``` json
{
  "status": "healthy"
}
```

------------------------------------------------------------------------

## POST /chat

Request

``` json
{
  "message": "Hello"
}
```

The endpoint must delegate all work to a service.

Response

``` json
{
  "response": "Hello from LangChain service!"
}
```

------------------------------------------------------------------------

# LangChain Service

Implement a class:

``` python
class LangChainService:

    async def invoke(self, message: str) -> str:
        return "Hello from LangChain service!"
```

Requirements

-   No OpenAI
-   No RAG
-   No embeddings
-   No vector database
-   No loaders

Only create the service abstraction that can easily be replaced
tomorrow.

------------------------------------------------------------------------

# Coding Rules

-   Async FastAPI
-   Full type hints
-   Small files
-   Clear separation of concerns
-   No business logic inside routes
-   Routes only call services
-   Use dependency injection where appropriate
-   Use pydantic-settings for configuration

------------------------------------------------------------------------

# Environment

Create

    OPENAI_API_KEY=
    OPENAI_MODEL=gpt-4.1-mini

Do not use them yet.

------------------------------------------------------------------------

# Tests

Implement

-   GET /health
-   POST /chat

All tests must pass with pytest.

------------------------------------------------------------------------

# Ruff

Configure Ruff.

CI must fail if Ruff fails.

------------------------------------------------------------------------

# GitHub Actions

## ci.yml

Trigger

-   pull_request
-   push

Run

1.  Checkout repository
2.  Setup Python 3.11
3.  Install uv
4.  uv sync
5.  Ruff
6.  pytest

The workflow must fail if linting or tests fail.

------------------------------------------------------------------------

## deploy.yml

Purpose

Automatically deploy the application to Azure App Service.

Trigger

``` yaml
on:
  push:
    branches:
      - main
```

Requirements

Deployment must execute **only if CI succeeds**.

Workflow should contain placeholders for:

-   AZURE_CLIENT_ID
-   AZURE_TENANT_ID
-   AZURE_SUBSCRIPTION_ID
-   AZURE_RESOURCE_GROUP
-   AZURE_WEBAPP_NAME

Use GitHub Actions with Azure Login via **OIDC**.

Do NOT use a Publish Profile.

Include placeholder steps for:

1.  Checkout
2.  Setup Python
3.  Install uv
4.  Build application
5.  Azure Login (placeholder)
6.  Deploy to Azure Web App (placeholder)

Leave Azure-specific values empty and clearly marked with TODO comments.

------------------------------------------------------------------------

# README

Include instructions for

-   uv installation
-   uv sync
-   Running locally
-   Running tests
-   Running Ruff
-   Environment variables
-   GitHub Actions
-   Azure deployment placeholders

------------------------------------------------------------------------

# Acceptance Criteria

The finished project must satisfy all of the following:

-   Runs with

``` bash
uv run uvicorn app.main:app --reload
```

-   GET /health returns healthy
-   POST /chat returns the LangChain service response
-   LangChain service is isolated from FastAPI
-   All tests pass
-   Ruff passes
-   CI runs automatically on every push and pull request
-   Every push to the **main** branch automatically triggers the
    deployment workflow
-   Deployment workflow is production-ready except Azure credentials and
    identifiers, which remain placeholders
-   Project structure is clean, minimal, and easy to extend with OpenAI
    and RAG tomorrow.
