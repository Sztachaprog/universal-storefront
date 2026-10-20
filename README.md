# Universal Storefront — Test Automation Framework

[![Tests](https://github.com/Sztachaprog/universal-storefront/actions/workflows/tests.yml/badge.svg)](https://github.com/Sztachaprog/universal-storefront/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Playwright](https://img.shields.io/badge/Playwright-E2E-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)

**71 automated tests across three layers (database integration, REST API with JWT, E2E UI), running in GitHub Actions on every push and pull request against an ephemeral PostgreSQL container, with an Allure report published as a build artifact.**

The system under test is a Flask + PostgreSQL VOD platform I built for this purpose: user accounts, a movie catalog, and three access tiers (free, premium, pay-per-view).

---

## Highlights

| | |
|---|---|
| **3-layer test pyramid** | 30 integration · 18 API · 23 E2E tests, each layer with its own isolation strategy |
| **Database as test oracle** | UI and API tests assert the resulting database state, not only what the screen or response shows |
| **Auth & access control** | JWT: expired, invalid and missing tokens; 401 vs 403 semantics; premium and PPV access enforced server-side |
| **Negative testing** | Tests on non-existent records exposed silent failures; fixed with `rowcount` validation |
| **CI** | GitHub Actions with a PostgreSQL service container, health checks, Flask readiness probe, secrets via GitHub Secrets |
| **Reporting** | Allure with full-page screenshots on E2E failure, uploaded as a CI artifact |

## Test architecture

| Layer | Tool | What it verifies | Isolation |
|---|---|---|---|
| Integration (`tests/database`) | pytest + psycopg2 | Business logic against real PostgreSQL: constraints, CRUD, access rules | Transaction rollback after each test |
| API (`tests/api`) | pytest + Requests | Status codes, JSON contracts, JWT auth, authorization per tier | `TRUNCATE` after each test |
| E2E (`tests/e2e`) | Playwright + Page Object Model | User flows in a real browser + DB state after UI actions | `TRUNCATE` after each test |

**Why rollback for integration but TRUNCATE for API/E2E?** Integration tests share the test's DB connection, so a rollback undoes everything. API and E2E tests go through the running Flask app, which commits on its own connection, so rollback in the test can't reach that data.

## CI pipeline

On every push and pull request to `main`:

1. PostgreSQL 16 starts as a service container (health-checked with `pg_isready`)
2. Integration tests run
3. Flask starts in the background; the job waits until `/login` responds (30 s timeout, logs printed on failure)
4. API and E2E (headless Chromium) tests run, each independent of the other's result
5. Allure report is generated and uploaded as an artifact, even when tests fail

`SECRET_KEY` is injected from GitHub Secrets; locally it is read from `.env` (not committed).

## Run locally

Requirements: Docker, Python 3.14, Poetry (optional: Allure CLI)

```bash
git clone https://github.com/Sztachaprog/universal-storefront.git
cd universal-storefront
poetry install
poetry run playwright install chromium

echo "SECRET_KEY=change-me" > .env
docker-compose up -d                                   # PostgreSQL on :5433, pgAdmin on :8080
poetry run python -m flask --app src.app run --port 5000

poetry run pytest tests/database                       # no Flask needed
poetry run pytest tests/api tests/e2e                  # Flask must be running
poetry run pytest tests --alluredir=allure-results && allure serve allure-results
```

> Credentials in `docker-compose.yml` are defaults for the local development database only.

## Tech stack

**Testing:** pytest, Playwright, Requests, Allure  
**Application:** Python, Flask, PostgreSQL, psycopg2, PyJWT, bcrypt  
**Infrastructure:** GitHub Actions, Docker Compose, Poetry

<details>
<summary>Project structure</summary>

```text
src/
  app.py               Flask routes, JWT decorator, API endpoints
  application.py       Business logic: users, movies, access control
  database/            Connection handling, schema.sql
tests/
  database/            Integration tests
  api/                 API tests
  e2e/                 E2E tests + pages/ (Page Objects)
.github/workflows/     CI pipeline
```
</details>

<details>
<summary>Database schema</summary>

- **users**: id, username (unique), email (unique), password_hash, is_premium, timestamps
- **movies**: id, release_date, is_premium_only
- **movie_translations**: movie_id → movies, language_code, title, description; unique (movie_id, language_code)
- **user_access** (pay-per-view): user_id → users, movie_id → movies, expires_at (default +30 days); unique (user_id, movie_id)

All foreign keys use `ON DELETE CASCADE`.
</details>

## Roadmap

- [ ] Containerize the Flask app (Dockerfile) and run the full stack with Docker Compose
- [ ] Publish the Allure report to GitHub Pages
- [ ] Static analysis (SAST) step in CI
- [ ] Parallel test execution
