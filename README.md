# Universal Storefront - QA Automation Framework
A portfolio project built to demonstrate multi-layer test automation across database, business logic, and UI levels. The project simulates a VOD streaming platform with user management, a movie catalog, and a premium subscription system

##  What This Project Tests
The framework covers three layers of testing:

- Integration tests — Python functions talking directly to PostgreSQL. Verify that data is correctly stored, updated, and deleted.
- E2E tests — Playwright opens a real browser, fills forms, clicks buttons, and checks what the user sees. Also verifies the database state after UI actions.
- CI/CD — GitHub Actions runs all tests automatically on every push to main.
- API tests — Requests library hits REST endpoints directly. Verifies status codes, JSON structure, and JWT authentication.

##  Tech Stack
- **Python 3.14**: Main language
- **Psycopg2**: Python driver for PostgreSQL
- **bcrypt**: Password hashing
- **PyJWT**: JWT token generation and validation
- **Requests**: HTTP client for API tests
- **Playwright**: Browser automation for E2E tests
- **Docker & Docker Compose**: Runs PostgreSQL in a container
- **Poetry**: Package manager
- **PostgreSQL**: Relational database
- **Flask**: Web framework
- **Pytest**: Test runner and fixture management
- **allure**: Pytest reporting with screenshots on failure
- **GitHub Actions**: CI/CD pipeline
  
##  Project Structure

```text
universal-storefront/
├── .github/
│   └── workflows/
│       └── tests.yml            # GitHub Actions CI/CD pipeline
├── src/
│   ├── database/
│   │   ├── sql/
│   │   │   └── schema.sql       # Database schema (tables, constraints)
│   │   ├── database.py          # DB connection management
│   │   └── db_utils.py          # Helper utilities
│   ├── static/
│   │   └── style.css            # Frontend styles
│   ├── templates/
│   │   ├── login.html           # Login page
│   │   ├── register.html        # Register page
│   │   └── dashboard.html       # Dashboard page 
│   ├── app.py                   # Flask application (routes, session management)
│   └── application.py           # Business logic (users, movies, access control)
├── tests/
│   ├── conftest.py              # Shared fixture: database schema setup
│   ├── api/
│   │   ├── conftest.py          # DB fixture: connection + TRUNCATE after each test
│   │   └── test_users_api.py    # API tests: CRUD + JWT auth scenarios
│   ├── database/
│   │   ├── conftest.py          # DB fixture: connection + rollback after each test
│   │   ├── test_user.py         # Integration tests: user registration, authentication, validation and profile management
│   │   ├── test_movie.py        # Integration tests: movie catalog
│   │   └── test_access.py       # Integration tests: PPV access + watch request logic
│   └── e2e/
│       ├── conftest.py          # E2E fixture: connection + TRUNCATE after each test
│       ├── pages/
│       │   ├── login_page.py    # Page Object: login page
│       │   ├── register_page.py # Page Object: register page
│       │   └── dashboard_page.py # Page Object: dashboard
│       ├── test_auth.py         # E2E: authentication flow
│       ├── test_register.py     # E2E: user registration flow
│       ├── test_login.py        # E2E: login flow
│       └── test_upgrade.py      # E2E: upgrade to premium + DB verification
├── docker-compose.yml
├── pyproject.toml
└── README.md
```


###  Database Schema

**Users**

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | SERIAL | PRIMARY KEY | Unique user identifier |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | User's display name |
| `password_hash` | TEXT | NOT NULL | Hashed user password |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | User's email address |
| `is_premium` | BOOLEAN | DEFAULT FALSE | Premium subscription status |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last profile update timestamp |

**Movies**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique movie identifier |
| `release_date` | DATE | | Movie release date |
| `is_premium_only` | BOOLEAN | DEFAULT FALSE | Whether movie requires premium subscription |

**Movie Translations**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique translation identifier |
| `movie_id` | INTEGER | NOT NULL, FK → movies(id) ON DELETE CASCADE | Reference to parent movie |
| `language_code` | VARCHAR(2) | NOT NULL | ISO 639-1 language code (e.g. `pl`, `en`) |
| `title` | VARCHAR(200) | NOT NULL | Localized movie title |
| `description` | TEXT | | Localized movie description |
| `movie_id + language_code` | | UNIQUE | One translation per language per movie |

**User Access**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique access record identifier |
| `user_id` | INTEGER | NOT NULL, FK → users(id) ON DELETE CASCADE | Reference to user |
| `movie_id` | INTEGER | NOT NULL, FK → movies(id) ON DELETE CASCADE | Reference to movie |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Access grant timestamp |
| `expires_at` | TIMESTAMP | DEFAULT NOW() + 30 days | Access expiry timestamp |
| `user_id + movie_id` | | UNIQUE | One access record per user per movie |


##  Quick Start

### 1. Requirements
- Docker Desktop
- Python 3.14
- Poetry
- Allure 

### 2. Setup
#### Clone the repository
- git clone https://github.com/Sztachaprog/universal-storefront.git
- cd universal-storefront

#### Install dependencies
- poetry install

#### Install Playwright browsers
- poetry run playwright install chromium

#### Install Allure CLI (for test reports)
   Windows (scoop):
   - scoop install allure
  
  macOS (brew):
   - brew install allure

#### Start PostgreSQL
- docker-compose up -d

#### Run the Application
- poetry run python -m flask --app src.app run --port 5000

- Then open http://localhost:5000 in your browser

### 3. Run Tests
#### All tests
- poetry run pytest tests

#### Integration tests only
- poetry run pytest tests/database

#### E2E tests only (Flask must be running)
- poetry run pytest tests/e2e

#### E2E with visible browser (Flask must be running)
- poetry run pytest tests/e2e --headed

#### API tests only (Flask must be running)
- poetry run pytest tests/api

### 4. Test Reports (Allure)
#### Generate results while running tests:
- poetry run pytest tests --alluredir=allure-results

#### Open the report:
- allure serve allure-results


## CI/CD
### GitHub Actions runs on every push to main:

1. Starts a PostgreSQL container (port 5433)
2. Installs Python 3.14 and Poetry
3. Installs dependencies and Playwright browsers
4. Runs integration tests
5. Starts Flask in the background
6. Runs API tests
7. Runs E2E tests with headless Chromium


## Status

This project is actively developed. Planned additions:
- Add /movies page
- Extended API, E2E tests
- Add mobile tests




