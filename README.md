# Book-Managing-App

A small project that provides both a Django web backend and a PyQt6 desktop application for managing books, authors, and quotes.

---

## Features ✅

- Manage authors, books, and quotes
- Full-text style searching for books and quotes
- Desktop UI implemented with PyQt6 (`BookStore/`)
- Web backend (Django) for additional features and integrations (`DjangoProject/`)

---

## Quick Start — Prerequisites ⚙️

- Python 3.11+ (tested with the included virtual environment)
- Windows (project developed on Windows; instructions below assume PowerShell)

---

## Installation & Setup 🔧

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv myenv
.\\myenv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Django DB (optional — used by web component):

```powershell
python manage.py migrate
```

Notes:
- The desktop app (PyQt6) uses a separate SQLite file named `books.db` created automatically by `BookStore/DB.py` when first run.
- The Django project uses `db.sqlite3` by default.

---

## Running the applications ▶️

- Run the Django web server (for web/API features):

```powershell
python manage.py runserver
```

- Run the desktop application (PyQt6):

```powershell
python BookStore/Main.py
```

---

## Tests 🧪

Run Django tests with:

```powershell
python manage.py test
```

The desktop UI does not include automated tests in this repository; manual testing and QA are recommended for UI flows.

---

## Development Notes 🔍

- The desktop UI code lives under `BookStore/` and follows a lightweight MVC-ish separation:
  - `DB.py` — database access layer (SQLite + helper methods)
  - `LogicLevel.py` — application logic / service layer
  - `Panel*` files — UI panels and forms
- The Django app is under `DjangoProject/` and uses the standard Django layout.

If you modify database access patterns, be careful to avoid executing the same query twice (this can insert duplicate rows).

---

## Contributing 🤝

- Open an issue to start a discussion for any substantive change.
- Submit PRs against `main` with a clear description of the change and tests where applicable.

---
