# Universal Storefront - QA Automation Framework

## 🎯 Cel projektu
Projekt został stworzony w celu nauki architektury systemów oraz automatyzacji testów na wielu poziomach (E2E). Symuluje on backend i frontend sklepu internetowego, łącząc testy bazy danych z testami UI.

## 🛠 Narzędzia i Technologie
- **Python 3.12+**: Główny język programowania (logika aplikacji).
- **Docker & Docker Compose**: Konteneryzacja bazy danych PostgreSQL.
- **Poetry**: Zarządzanie zależnościami i środowiskiem wirtualnym.
- **PostgreSQL**: Relacyjna baza danych.
- **Pytest**: Framework do uruchamiania i raportowania testów.
- **Psycopg2**: Sterownik do komunikacji Pythona z bazą SQL.
- **Playwright**: (W trakcie wdrażania) Automatyzacja testów UI w przeglądarce.
- **GitHub Actions**: (W trakcie wdrażania) Automatyzacja testów (CI/CD) przy każdej zmianie w kodzie.

## 🏗 Struktura projektu

```text
UNIVERSAL-STOREFRONT/
├── src/                          # Serce aplikacji (Logika biznesowa)
│   ├── database/                 # Folder baz danych
│   │   ├── sql/                  # Skrypty SQL (inicjalizacja bazy)
│   │   │   ├── schema.sql        # Definicja tabel
│   │   │   └── seed.sql          # Przykładowe dane startowe
│   │   ├── database.py           # Zarządzanie połączeniem z PostgreSQL (DRY)
│   │   └── db_utils.py           # Narzędzia pomocnicze do operacji na bazie
│   └── application.py            # Główne funkcje aplikacji
├── tests/                        # Folder testowy (Pytest)
│   ├── database/                 # Testy integracyjne bazy danych
│   │   └── test_user.py          # Testy logiki użytkowników
│   └── conftest.py               # Konfiguracja i fixture'y dla testów
├── .gitignore                    # Pliki ignorowane przez Git
├── docker-compose.yml            # Definicja kontenera z bazą danych
├── pyproject.toml                # Konfiguracja Poetry i zależności
└── README.md                     # Dokumentacja projektu
```


### 🗄️ Schemat bazy danych

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

## 🚀 Szybki Start

### 1. Wymagania wstępne
Upewnij się, że masz zainstalowane:
- Docker Desktop
- Python 3.12+
- Poetry

### 2. Instalacja i uruchomienie
# Sklonuj projekt
git clone <url-twojego-repozytorium>

# Zainstaluj biblioteki przez Poetry
poetry install

# Uruchom bazę danych w Dockerze
docker-compose up -d
 Uruchom wszystkie testy z logami w terminalu
poetry run pytest -s



​💡 Rozwiązywane problemy
​Port bazy danych: Projekt korzysta z portu 5433, aby uniknąć konfliktów z lokalnymi instalacjami PostgreSQL





