# Quick Start Guide - Быстрый старт

## Быстрая установка и первый запуск

### 1. Подготовка

```bash
# Перейти в директорию проекта
cd dnevnik-api

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt
```

### 2. Конфигурация

```bash
# Копировать пример конфига
copy .env.example .env

# Убедитесь что PostgreSQL запущена и создана база данных:
# createdb dnevnik_db
```

### 3. Инициализация базы данных

```bash
# Применить миграции
python manage.py migrate

# Создать администратора
python manage.py createsuperuser
# Введите:
# Username: admin
# First name: Admin
# Last name: User
# Email: admin@example.com
# Password: (введите пароль)
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен на: **http://localhost:8000**

## Первые шаги в API

### 1. Вход в администрацию Django

Перейдите на http://localhost:8000/admin/ и используйте учетные данные суперпользователя

### 2. Просмотр документации API

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/schema/

### 3. Получить JWT токен

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "ваш_пароль"}'
```

Ответ:
```json
{
  "access": "ваш_access_token",
  "refresh": "ваш_refresh_token",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### 4. Использование токена в запросах

```bash
# Сохраните access токен в переменную
$token = "ваш_access_token"

# Используйте в запросах
curl -X GET http://localhost:8000/api/v1/academics/subjects/ \
  -H "Authorization: Bearer $token"
```

## Создание тестовых данных

### 1. Создать предметы

```bash
# Через админ панель: http://localhost:8000/admin/academics/subject/
# или через API:

curl -X POST http://localhost:8000/api/v1/academics/subjects/ \
  -H "Authorization: Bearer $token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Математика", "description": "Основной курс математики"}'
```

### 2. Создать группу

```bash
curl -X POST http://localhost:8000/api/v1/academics/groups/ \
  -H "Authorization: Bearer $token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "10-A",
    "academic_year": "2024-2025",
    "description": "Десятый класс, группа А"
  }'
```

### 3. Создать пользователей

```bash
# Создать учителя
curl -X POST http://localhost:8000/api/v1/admin/users/ \
  -H "Authorization: Bearer $token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teacher1",
    "password": "TeacherPass123",
    "first_name": "Иван",
    "last_name": "Сидоров",
    "email": "teacher1@example.com",
    "role": "teacher"
  }'

# Создать студента
curl -X POST http://localhost:8000/api/v1/admin/users/ \
  -H "Authorization: Bearer $token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "StudentPass123",
    "first_name": "Петр",
    "last_name": "Иванов",
    "email": "student1@example.com",
    "role": "student"
  }'
```

### 4. Привязать студента к группе

Через админ панель перейти в Students и создать профиль студента с привязкой к группе.

### 5. Создать расписание

```bash
curl -X POST http://localhost:8000/api/v1/academics/schedules/ \
  -H "Authorization: Bearer $token" \
  -H "Content-Type: application/json" \
  -d '{
    "group": 1,
    "subject": 1,
    "teacher": 1,
    "weekday": 0,
    "start_time": "09:00",
    "end_time": "10:00",
    "room": "101"
  }'
```

## Важные команды Django

```bash
# Создать миграции после изменения моделей
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Показать миграции
python manage.py showmigrations

# Откатить миграции
python manage.py migrate apps.accounts 0001

# Собрать статические файлы
python manage.py collectstatic

# Запустить оболочку Django
python manage.py shell

# Создать кэш-таблицу для сессий
python manage.py createcachetable

# Проверить конфигурацию
python manage.py check
```

## Структура файлов приложений

Каждое приложение содержит:

```
apps/app_name/
├── __init__.py
├── admin.py          # Регистрация в админ панели
├── apps.py           # Конфигурация приложения
├── models.py         # ORM модели
├── serializers.py    # DRF сериализаторы
├── views.py          # ViewSets и Views
├── urls.py           # URL маршруты
├── tests.py          # Тесты (если есть)
└── migrations/       # Миграции БД
    └── 0001_initial.py
```

## Типичный рабочий процесс

1. **Определить модель** в `models.py`
2. **Создать сериализатор** в `serializers.py`
3. **Создать ViewSet** в `views.py`
4. **Зарегистрировать в URL** в `urls.py`
5. **Зарегистрировать в админ панели** в `admin.py`
6. **Создать миграцию**: `python manage.py makemigrations`
7. **Применить миграцию**: `python manage.py migrate`
8. **Протестировать** через API

## Отладка

### Включить детальное логирование

В `settings.py` установите:

```python
DEBUG = True
LOGGING['root']['level'] = 'DEBUG'
```

### Просмотреть SQL запросы

```python
# В manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    # Ваш код
    pass

for query in queries:
    print(query['sql'])
```

## Полезные ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/)

## Решение распространенных проблем

### "No such table" ошибка

```bash
# Миграции не применены
python manage.py migrate
```

### "ModuleNotFoundError"

```bash
# Переустановить зависимости
pip install --force-reinstall -r requirements.txt
```

### "Connection refused" для PostgreSQL

```bash
# Убедитесь что PostgreSQL запущена и правильно настроена в .env
```

### Ошибка CORS

Добавьте правильные origins в `.env`:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

**Готово!** Теперь вы можете начать разработку.
