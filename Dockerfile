FROM python:3.11-slim

WORKDIR /app

# Установить системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установить Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копировать проект
COPY . .

# Создать необходимые директории
RUN mkdir -p /app/logs /app/media /app/staticfiles

# Сделать manage.py исполняемым
RUN chmod +x manage.py

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn dnevnik_project.wsgi:application --bind 0.0.0.0:8000"]
