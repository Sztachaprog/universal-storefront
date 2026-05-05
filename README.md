# Universal Storefront - QA Automation Framework

##  Cel projektu
Projekt został stworzony w celu nauki architektury systemów oraz automatyzacji testów na wielu poziomach (E2E). Symuluje on backend i frontend sklepu internetowego, łącząc testy bazy danych z testami UI.

##  Narzędzia i Technologie
- **Python 3.12+**: Główny język programowania (logika aplikacji).
- **Docker & Docker Compose**: Konteneryzacja bazy danych PostgreSQL.
- **Poetry**: Zarządzanie zależnościami i środowiskiem wirtualnym.
- **PostgreSQL**: Relacyjna baza danych.
- **Pytest**: Framework do uruchamiania i raportowania testów.
- **Psycopg2**: Sterownik do komunikacji Pythona z bazą SQL.
- **Playwright**: (W trakcie wdrażania) Automatyzacja testów UI w przeglądarce.
- **GitHub Actions**: (W trakcie wdrażania) Automatyzacja testów (CI/CD) przy każdej zmianie w kodzie.

##  Struktura projektu

```text
UNIVERSAL-STOREFRONT/
├── src/                         			# Kod źródłowy aplikacji
│   ├── database/                 			# Warstawa dostępu do danych (połączenie, zapytania SQL)
│   │   ├── sql/                  			# Skrypty SQL (inicjalizacja bazy)
│   │   │   └── schema.sql                  # Przykładowe dane startowe
│   │   ├── database.py           			# Zarządzanie połączeniem z PostgreSQL
│   │   └── db_utils.py           			# Narzędzia pomocnicze do operacji na bazie
│   ├── __init__.py               			# Umożliwenie importu src/ między modułami
│   ├── app.py                   			# Serwer Flask - (UI)
│   └── application.py           			# Główne funkcje aplikacji
├── tests/                       			# Folder testowy (Pytest)
│   ├── database/                			# Testy integracyjne bazy danych
│   │   ├── test_access.py             		# Testy logiki dostępów
│   │   ├── test_movie.py         			# Testy logiki filmów
│   │   └── test_user.py         			# Testy logiki użytkowników
│   └── conftest.py             			# Konfiguracja i fixture'y dla testów
├── .gitignore                   			# Pliki ignorowane przez Git
├── docker-compose.yml           			# Definicja kontenera z bazą danych
├── pyproject.toml               			# Konfiguracja Poetry i zależności
└── README.md                    			# Dokumentacja projektu
```


###  Schemat bazy danych

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


##  Szybki Start

### 1. Wymagania wstępne
Upewnij się, że masz zainstalowane:
- Docker Desktop
- Python 3.12+
- Poetry

### 2. Instalacja i uruchomienie
#### Sklonuj projekt
git clone https://github.com/Sztachaprog/universal-storefront.git

#### Zainstaluj biblioteki przez Poetry
poetry install

#### Uruchom bazę danych w Dockerze
docker-compose up -d
 
#### Uruchom wszystkie testy z logami w terminalu
poetry run pytest -s



​ Rozwiązane problemy

​Port bazy danych: Projekt korzysta z portu 5433, aby uniknąć konfliktów z lokalnymi instalacjami PostgreSQL





