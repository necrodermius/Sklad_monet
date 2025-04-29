# Base Image
FROM python:3.11-slim

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Робоча директорія
WORKDIR /app

# Встановлюємо залежності
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копіюємо код
COPY . .

# Використовуємо Gunicorn для запуску Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
