# Brain - Graph-based notes app

Backend for a graph-based note system with both HTTP API and Telegram bot entrypoints. Notes, keywords, and wikilinks are stored in Postgres, graph relationships are maintained in Neo4j, and uploads are stored in an S3-compatible bucket (MinIO in local dev). Redis is used for caching/auxiliary data.

## Architecture

This project follows a layered (clean) architecture with explicit dependency direction: infrastructure → application → domain.

- `brain/domain`: core entities and pure domain services (no frameworks, no persistence).
- `brain/application`:
  - `interactors`: thin use cases (one action each) that orchestrate workflows.
  - `services`: reusable business rules shared across use cases.
  - `abstractions`: repository interfaces and config contracts.
- `brain/infrastructure`: concrete implementations (DB repositories, graph repo, JWT/S3 clients).
- `brain/presentation`:
  - `api`: FastAPI routes, schemas, mappers, and dependencies.
  - `tgbot`: Aiogram handlers, dialogs, and middleware.
- `brain/main/entrypoints`: application entrypoints and DI wiring (Dishka providers).

Typical request flow: presentation layer calls an interactor → interactor uses domain services + repository interfaces → infrastructure provides implementations and persists data.

## Local development

This repo relies on [uv](https://github.com/astral-sh/uv).

1. Install uv (see the uv README for the preferred installer on your platform).
2. Create/sync the virtual environment: `uv sync` (or `make venv`). This command creates `.venv` and installs everything defined in `pyproject.toml`.
3. Run commands through uv so the managed interpreter is used, e.g. `uv run pytest tests --disable-warnings -s` or use the provided `make test` target.
4. After changing dependencies run `uv lock` (or `uv sync --locked`) and commit the updated `uv.lock`.

## Tests

Tests are split by scope:

- `tests/integration`: integration tests
- `tests/unit`: unit tests
- `tests/e2e`: e2e tests
  
Run the full suite:

```bash
pytest tests --disable-warnings -s
```

### Test coverage

Run coverage:

```bash
pytest tests --cov=brain --cov-report=term-missing
```

