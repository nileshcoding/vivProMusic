# VivPro Music API

A high‑performance **Music Discovery and Rating API** built with **Django REST Framework**, **PostgreSQL (GiST Trigram Indexing)**, and **Celery**.

---

## Architecture Overview

This project is optimized for **fast reads** (searching songs) and **instant user interactions** (submitting ratings):

* **PostgreSQL + pg_trgm (GiST Trigram Indexing)**
  Enables extremely fast partial text searches (e.g. `LIKE %term%`) across large song catalogs.

* **Denormalized Music Model**
  The `Music` table stores `average_rating` and `total_ratings` to avoid expensive aggregations during list/search requests.

* **Asynchronous Workers (Celery + Redis)**
  Rating recalculations run in the background so API responses stay fast and predictable.

---

## Project Structure

```text
vivProMusic/
├── manage.py
├── playlist.json               # Source data (columnar JSON)
├── requirements.txt
├── music_project/              # Project core
│   ├── __init__.py             # Loads Celery app
│   ├── settings.py             # Global config (DB, Redis, JWT)
│   ├── urls.py                 # Root URL router
│   ├── celery.py               # Celery app definition
│   └── wsgi.py                 # WSGI entrypoint
└── music_app/                  # Main application
    ├── admin/
    │   ├── __init__.py
    │   └── music.py            # Admin panel customization
    ├── management/
    │   └── commands/
    │       └── load_music.py   # Columnar JSON loader command
    ├── migrations/             # DB migrations (includes pg_trgm)
    ├── models/
    │   └── music.py            # Music & Rating models
    ├── serializers/
    │   ├── music.py
    │   └── rating.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_music.py       # Tests (must start with `test_`)
    ├── views/
    │   ├── music.py            # Read‑optimized search ViewSet
    │   └── rating.py           # POST‑only rating endpoint
    └── tasks.py                # Celery background tasks
```

---

## Tech Stack

* **Framework**: Django, Django REST Framework
* **Database**: PostgreSQL (`pg_trgm` extension enabled)
* **Message Broker**: Redis (AWS ElastiCache in production)
* **Task Queue**: Celery
* **Authentication**: JWT (SimpleJWT)

---

## Key Components

* `music_app/management/commands/load_music.py`
  Custom Django command to ingest columnar Spotify JSON data.

* `music_app/tasks.py`
  Celery tasks responsible for recalculating ratings asynchronously.

* `music_app/views/music.py`
  Read‑optimized endpoints for listing and searching music.

* `music_app/views/rating.py`
  Write‑optimized POST‑only endpoint for submitting ratings.

* `music_project/celery.py`
  Central Celery configuration and app initialization.

---

## Getting Started

### 1. Environment Setup

Activate your virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Enable trigram support in PostgreSQL:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

Run migrations and load initial music data:

```bash
python manage.py migrate
python manage.py load_music playlist.json
```

---

## Running the Application Locally

To run the full system, ensure the virtual environment is active in **each** terminal tab.

### 1. Start Redis (Message Broker)

```bash
# Terminal 1
redis-server
```

### 2. Start Django API Server

```bash
# Terminal 2
python manage.py runserver
```

### 3. Start Celery Worker

```bash
# Terminal 3
celery -A music_project worker --loglevel=info
```

---

## Notes

* Rating updates are eventually consistent by design.
* Search performance relies on PostgreSQL trigram indexes — ensure `pg_trgm` is enabled in all environments.
* Celery workers must be running for rating aggregation to work correctly.
