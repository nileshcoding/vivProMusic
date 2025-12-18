# VivPro Music API

A high-performance Music Discovery and Rating API built with Django REST Framework, PostgreSQL (GiST Trigram Indexing), and Celery.

## Architecture Overview
To ensure high-performance reads (searching songs) and fast user interactions (submitting ratings), this project uses:
* **PostgreSQL with GiST Trigram Indexing**: Allows for extremely fast partial text searches (`LIKE %term%`) across thousands of song titles.
* **Denormalized Music Model**: The `Music` table stores `average_rating` and `total_ratings` as columns to avoid expensive on-the-fly calculations during list/search requests.
* **Asynchronous Workers (Celery + Redis)**: Rating calculations are offloaded to background workers, ensuring the API responds instantly to users.

---
# Project Structure
vivProMusic/
├── manage.py
├── playlist.json              # Source Data (Columnar JSON)
├── requirements.txt
├── music_project/             # Project Core
│   ├── __init__.py            # Loads Celery app
│   ├── settings.py            # Global Config (DB, Redis, JWT)
│   ├── urls.py                # Main URL router
│   └── celery.py              # Celery instance definition
│   └── wsgi.py                # server gateway
└── music_app/                 # Main Application
    ├── admin/
    │   ├── __init__.py        # Exposes Music & Rating Admin
    │   └── music.py           # Admin Panel Customization
    ├── management/
    │   └── commands/
    │       └── load_music.py  # Columnar JSON Parser
    ├── migrations/            # Migration history (includes pg_trgm)
    ├── models/
    │   └── music.py           # Music & Rating schemas
    ├── serializers/
    │   ├── music.py
    │   └── rating.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_music.py      # MUST start with 'test_' for discovery
    ├── views/
    │   ├── music.py           # Read-optimized search ViewSet
    │   └── rating.py          # POST-only rating ViewSet
    └── tasks.py               # Celery background tasks

---

## Tech Stack
- **Framework**: Django & Django REST Framework
- **Database**: PostgreSQL (with `pg_trgm` extension)
- **Broker**: Redis (running on AWS ElastiCache for production)
- **Task Queue**: Celery
- **Auth**: JWT (SimpleJWT)

---

## Project Structure
- `music_app/management/commands/load_music.py`: Custom command to load columnar Spotify JSON data.
- `music_app/tasks.py`: Background tasks for rating recalculations.
- `music_app/views/rating.py`: ReadOnly
- `music_app/views/rating.py`: POST-only endpoint
- `music_project/celery.py`: Celery application configuration.

---

## Getting Started

### 1. Environment Setup
Activate your virtual environment and install dependencies:
```bash
source .venv/bin/activate
pip install -r requirements.txt

# In psql shell
CREATE EXTENSION IF NOT EXISTS pg_trgm;

# In terminal
python manage.py migrate

python manage.py load_music playlist.json

## Running the Application locally

To run the full system, ensure your virtual environment is active in each terminal tab (`source .venv/bin/activate`).

### 1. Start the Redis Broker
The broker must be running first so that Django and Celery can communicate.
```bash
# Terminal 1
redis-server

# Terminal 2
python manage.py runserver

# Terminal 3
celery -A music_project worker --loglevel=info
