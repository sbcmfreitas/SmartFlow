FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if needed) and Poetry
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Project initialization:
# 1. Disable virtualenv creation to install directly in system python
# 2. Install dependencies (no-root to avoid installing the app itself as a package yet)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
