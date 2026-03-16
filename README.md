# universal-storefront

# 🛒 Universal Storefront - QA Automation Framework

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

## 🏗 Struktura projektu
- `src/`: Logika biznesowa (tzw. "mózg"). Tu znajdą się funkcje zarządzające bazą i produktami.
- `tests/`: Scenariusze testowe (database, integration, ui).
- `docker-compose.yml`: Konfiguracja infrastruktury bazy danych.

## 🚀 Szybki Start

### 1. Wymagania wstępne
Upewnij się, że masz zainstalowane:
- Docker Desktop
- Python 3.12+
- Poetry

### 2. Instalacja i uruchomienie
``bash
# Sklonuj projekt
git clone <url-twojego-repozytorium>

# Zainstaluj biblioteki przez Poetry
poetry install

# Uruchom bazę danych w Dockerze
docker-compose up -d
 Uruchom wszystkie testy z logami w terminalu
poetry run pytest -s

​💡 Rozwiązywanie problemów
​Port bazy danych: Projekt korzysta z portu 5433, aby uniknąć konfliktów z lokalnymi instalacjami PostgreSQL.
​Błąd uprawnień Git: Jeśli przenosisz projekt między komputerami, użyj komendy:
git config --global --add safe.directory <sciezka_do_projektu>
​Reset danych: Aby wyczyścić bazę i zacząć od zera, użyj: docker-compose down -v.









# 🛒 Universal Storefront - QA Automation Framework

## 🎯 Project Goal
This project is an End-to-End (E2E) automated testing framework designed to learn system architecture and full-stack automation. It simulates an e-commerce backend and frontend, verifying database integrity, business logic, and UI behavior.

## 🛠 Tech Stack
- **Python 3.12+**: Core logic and test scripting.
- **Docker & Docker Compose**: Infrastructure isolation (PostgreSQL container).
- **Poetry**: Dependency management and virtual environment control.
- **PostgreSQL**: Relational database for storing users and products.
- **Pytest**: Test runner for executing and reporting tests.
- **Psycopg2**: Database driver for Python-to-SQL communication.
- **Playwright**: (Work in Progress) UI automation for browser-based testing.

## 🏗 Project Structure
- `src/`: The "Brain" of the app. Contains database managers and core business logic.
- `tests/`: Test suites divided by layer (database, integration, and UI).
- `docker-compose.yml`: Infrastructure-as-code for the database environment.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed:
- **Docker Desktop**
- **Python 3.12+**
- **Poetry**

### 2. Installation & Setup
```bash
# Clone the repository
git clone <your-repository-url>

# Install dependencies via Poetry
poetry install

# Spin up the database container
docker-compose up -d


# Run all tests with console output
poetry run pytest -s


🗄 Database Schema
​Table: users

Column Type Description
id Serial Primary Key (Auto-increment)
username Varchar(50) User's display name
is_premium Boolean Premium status (Default: False)

💡 Troubleshooting
​Port Conflict: This project uses port 5433 to avoid conflicts with local PostgreSQL instances running on port 5432.
​Git Security Error: If moving the project between machines, you might see a "dubious ownership" error. Fix it with:
git config --global --add safe.directory <project_path>
​Database Reset: To wipe all data and start fresh, run:
docker-compose down -v
