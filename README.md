# Film API

Учебный REST API для управления коллекцией фильмов, разработанный на FastAPI.

## Features

- Создание, получение, обновление и удаление фильмов (CRUD)
- Фильтрация фильмов по названию, жанру, режиссёру и году выпуска
- Пагинация и сортировка
- Загрузка и хранение постеров
- Документация API через Swagger UI
- Тестирование с помощью pytest и HTTPX

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest
- HTTPX

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/film-api.git
cd film-api

python -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn src.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Tests

```bash
python -m pytest -v
```

## Status

Educational project in development.
