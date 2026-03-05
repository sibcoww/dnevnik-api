# Dnevnik API - Online School Journal System

Полнофункциональный Django REST API для системы электронного журнала, используемой частными школами для управления студентами, преподавателями, расписанием, оценками и домашним заданием.

## 🚀 Технический стек

- **Python 3.11**
- **Django 4.2.8**
- **Django REST Framework 3.14.0**
- **PostgreSQL**
- **JWT Authentication (SimpleJWT 5.3.2)**
- **Django CORS Headers**
- **DRF Spectacular (OpenAPI/Swagger)**

## 📋 Структура проекта

```
dnevnik-api/
├── dnevnik_project/          # Django проект
│   ├── settings.py           # Конфигурация
│   ├── urls.py              # URL маршруты
│   ├── wsgi.py              # WSGI конфигурация
│   └── asgi.py              # ASGI конфигурация
├── apps/
│   ├── core/                # Общие утилиты и базовые модели
│   ├── accounts/            # Управление пользователями и ролями
│   ├── academics/           # Предметы, группы, расписание, уроки
│   ├── journal/             # Посещаемость и оценки
│   ├── homework/            # Домашнее задание и материалы
│   └── exams/               # Экзамены и результаты
├── manage.py                # Django управление
├── requirements.txt         # Python зависимости
└── .env.example            # Пример переменных окружения
```

## 🔐 Система ролей

Система поддерживает следующие роли пользователей:

1. **student** - Студент
2. **teacher** - Преподаватель
3. **academic_office** - Академический офис
4. **admin** - Администратор
5. **director** - Директор

### Модель пользователя

```python
User
├── id (BigAutoField)
├── username (CharField, уникальный)
├── password (зашифрованный)
├── first_name
├── last_name
├── email
├── role (выбор из ролей выше)
├── is_active
├── date_joined
└── is_staff, is_superuser
```

## 📚 Основные модели

### Academics (Учебный процесс)

- **Subject** - Предмет
- **Group** - Группа/класс студентов
- **Schedule** - Расписание занятий
- **Lesson** - Урок (конкретное занятие)
- **TeacherSubject** - Связь учителя с предметом

### Journal (Журнал)

- **Attendance** - Посещаемость (present, absent, late, excused_absence)
- **Grade** - Оценка (homework, classwork, test, exam, project, quiz)
- **StudentGradeAverage** - Средняя оценка студента

### Homework (Домашнее задание)

- **Homework** - Домашнее задание
- **HomeworkMaterial** - Материалы (файлы и ссылки)
- **StudentHomeworkSubmission** - Сдача домашнего задания студентом

### Exams (Экзамены)

- **Exam** - Экзамен
- **ExamResult** - Результат экзамена
- **ExamQuestion** - Вопрос экзамена (опционально)

## 🔌 API эндпойнты

### Аутентификация

```
POST   /api/v1/auth/login              - Вход (получить JWT токены)
POST   /api/v1/auth/refresh            - Обновить access токен
GET    /api/v1/auth/users/me/          - Получить данные текущего пользователя
```

### Управление учебными данными

**Предметы:**
```
GET    /api/v1/academics/subjects/     - Список предметов
GET    /api/v1/academics/subjects/{id}/
```

**Группы:**
```
GET    /api/v1/academics/groups/       - Список групп
POST   /api/v1/academics/groups/       - Создать группу (академический офис)
GET    /api/v1/academics/groups/{id}/
PATCH  /api/v1/academics/groups/{id}/
DELETE /api/v1/academics/groups/{id}/
```

**Расписание:**
```
GET    /api/v1/academics/schedules/              - Список расписаний
POST   /api/v1/academics/schedules/              - Создать (академический офис)
GET    /api/v1/academics/schedules/{id}/
GET    /api/v1/academics/schedules/by_group/    - По группе
GET    /api/v1/academics/schedules/by_teacher/  - По учителю
PATCH  /api/v1/academics/schedules/{id}/
```

**Уроки:**
```
GET    /api/v1/academics/lessons/                 - Список уроков
POST   /api/v1/academics/lessons/                 - Создать (учитель)
GET    /api/v1/academics/lessons/{id}/
GET    /api/v1/academics/lessons/today/           - Уроки на сегодня
GET    /api/v1/academics/lessons/by_group/       - По группе
GET    /api/v1/academics/lessons/by_teacher/     - По учителю
GET    /api/v1/academics/lessons/upcoming/       - Предстоящие уроки
```

### Журнал посещаемости и оценки

**Посещаемость:**
```
GET    /api/v1/journal/attendance/                - Список
POST   /api/v1/journal/attendance/                - Создать (учитель)
POST   /api/v1/journal/attendance/bulk_create/    - Массовое создание
GET    /api/v1/journal/attendance/by_student/    - По студенту
GET    /api/v1/journal/attendance/statistics/    - Статистика посещаемости
PATCH  /api/v1/journal/attendance/{id}/
```

**Оценки:**
```
GET    /api/v1/journal/grades/                          - Список
POST   /api/v1/journal/grades/                          - Создать (учитель)
GET    /api/v1/journal/grades/{id}/
GET    /api/v1/journal/grades/by_student/              - По студенту
GET    /api/v1/journal/grades/by_subject/              - По предмету
GET    /api/v1/journal/grades/average_by_student_subject/  - Средняя
PATCH  /api/v1/journal/grades/{id}/
```

### Домашнее задание

**Домашнее задание:**
```
GET    /api/v1/homework/homeworks/                   - Список
POST   /api/v1/homework/homeworks/                   - Создать (учитель)
GET    /api/v1/homework/homeworks/{id}/
GET    /api/v1/homework/homeworks/upcoming/         - Предстоящие
GET    /api/v1/homework/homeworks/by_group/        - По группе
GET    /api/v1/homework/homeworks/by_subject/      - По предмету
PATCH  /api/v1/homework/homeworks/{id}/
```

**Материалы домашнего задания:**
```
GET    /api/v1/homework/materials/              - Список
POST   /api/v1/homework/materials/              - Создать (учитель)
GET    /api/v1/homework/materials/{id}/
DELETE /api/v1/homework/materials/{id}/
```

**Сдача домашнего задания:**
```
GET    /api/v1/homework/submissions/                - Список
POST   /api/v1/homework/submissions/                - Создать (студент)
GET    /api/v1/homework/submissions/{id}/
GET    /api/v1/homework/submissions/my_submissions/ - Мои сдачи
GET    /api/v1/homework/submissions/pending/       - Ожидающие проверки
GET    /api/v1/homework/submissions/overdue/       - Просроченные
POST   /api/v1/homework/submissions/{id}/submit/   - Сдать
PATCH  /api/v1/homework/submissions/{id}/         - Оценить (учитель)
```

### Экзамены

**Экзамены:**
```
GET    /api/v1/exams/exams/                    - Список
POST   /api/v1/exams/exams/                    - Создать (учитель)
GET    /api/v1/exams/exams/{id}/
GET    /api/v1/exams/exams/upcoming/           - Предстоящие
GET    /api/v1/exams/exams/by_group/          - По группе
GET    /api/v1/exams/exams/by_subject/        - По предмету
POST   /api/v1/exams/exams/{id}/start/        - Начать экзамен
POST   /api/v1/exams/exams/{id}/complete/     - Завершить экзамен
PATCH  /api/v1/exams/exams/{id}/
```

**Результаты экзаменов:**
```
GET    /api/v1/exams/results/                        - Список
POST   /api/v1/exams/results/                        - Создать результат
GET    /api/v1/exams/results/{id}/
GET    /api/v1/exams/results/my_results/            - Мои результаты
GET    /api/v1/exams/results/by_exam/               - По экзамену
GET    /api/v1/exams/results/statistics/            - Статистика
PATCH  /api/v1/exams/results/{id}/                  - Оценить
```

### Управление пользователями (администраторы)

```
GET    /api/v1/admin/users/                  - Список пользователей
POST   /api/v1/admin/users/                  - Создать пользователя
GET    /api/v1/admin/users/{id}/
PATCH  /api/v1/admin/users/{id}/            - Обновить пользователя
DELETE /api/v1/admin/users/{id}/            - Удалить пользователя
```

## 🔐 Система прав доступа

| Операция | Student | Teacher | Academic Office | Admin | Director |
|----------|---------|---------|-----------------|-------|----------|
| Просмотр собственных данных | ✅ | ✅ | ✅ | ✅ | ✅ |
| Создание расписания | ❌ | ❌ | ✅ | ❌ | ❌ |
| Создание оценок | ❌ | ✅ | ❌ | ❌ | ❌ |
| Создание посещаемости | ❌ | ✅ | ❌ | ❌ | ❌ |
| Управление пользователями | ❌ | ❌ | ❌ | ✅ | ❌ |
| Просмотр аналитики | ❌ | ❌ | ❌ | ❌ | ✅ |

## 📦 Установка

### Требования

- Python 3.11+
- PostgreSQL 12+
- pip

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd dnevnik-api
```

### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Конфигурация переменных окружения

```bash
# Скопируйте пример конфига
cp .env.example .env

# Отредактируйте .env с вашими параметрами
```

### 5. Создание базы данных PostgreSQL

```bash
# Windows (если psql в PATH)
createdb dnevnik_db

# Linux/Mac
createdb dnevnik_db

# или через psql
psql -U postgres
CREATE DATABASE dnevnik_db;
```

### 6. Миграции базы данных

```bash
python manage.py migrate
```

### 7. Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

### 8. Сбор статических файлов

```bash
python manage.py collectstatic
```

### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен на `http://localhost:8000`

## 📖 API Документация

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/schema/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔑 Аутентификация

### Получение токенов

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "username", "password": "password"}'
```

**Ответ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "role": "teacher"
  }
}
```

### Использование токена

Добавьте заголовок `Authorization` в запросы:

```bash
curl -X GET http://localhost:8000/api/v1/academics/groups/ \
  -H "Authorization: Bearer <access_token>"
```

## 📝 Примеры использования

### 1. Создание нового студента (администратор)

```bash
curl -X POST http://localhost:8000/api/v1/admin/users/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "SecurePass123",
    "first_name": "Ivan",
    "last_name": "Petrov",
    "email": "ivan@example.com",
    "role": "student"
  }'
```

### 2. Создание группы (академический офис)

```bash
curl -X POST http://localhost:8000/api/v1/academics/groups/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "10-A",
    "academic_year": "2024-2025",
    "description": "Группа 10-А"
  }'
```

### 3. Создание расписания (академический офис)

```bash
curl -X POST http://localhost:8000/api/v1/academics/schedules/ \
  -H "Authorization: Bearer <token>" \
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

### 4. Создание оценки (учитель)

```bash
curl -X POST http://localhost:8000/api/v1/journal/grades/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "subject": 1,
    "teacher": 1,
    "value": 5,
    "grade_type": "test",
    "comment": "Хорошо выполнена работа"
  }'
```

### 5. Получение посещаемости студента

```bash
curl -X GET "http://localhost:8000/api/v1/journal/attendance/by_student/?student_id=1" \
  -H "Authorization: Bearer <token>"
```

## 🚀 Развертывание

### Используя Gunicorn

```bash
pip install gunicorn
gunicorn dnevnik_project.wsgi:application --bind 0.0.0.0:8000
```

### Используя Docker (опционально)

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "dnevnik_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Постройте и запустите:

```bash
docker build -t dnevnik-api .
docker run -p 8000:8000 dnevnik-api
```

## 📊 Производительность

### Рекомендуемая конфигурация PostgreSQL для продакшена

```sql
-- Увеличиваем параметры для лучшей производительности
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET max_wal_size = '1GB';
```

### Оптимизация запросов

- Используйте `select_related()` для ForeignKey
- Используйте `prefetch_related()` для ManyToMany и reverse ForeignKey
- Добавьте индексы на часто используемые поля поиска

## 🔍 Поиск и фильтрация

Все эндпойнты поддерживают фильтрацию через query параметры:

```bash
# Фильтр по группе
GET /api/v1/academics/lessons/?schedule__group=1

# Поиск по имени
GET /api/v1/accounts/students/?search=Ivan

# Сортировка
GET /api/v1/journal/grades/?ordering=-value
```

## 📋 Пагинация

По умолчанию: 20 результатов на странице

```bash
GET /api/v1/academics/groups/?page=2
```

## 🧪 Тестирование

```bash
# Запуск тестов
python manage.py test

# С покрытием
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📝 Логирование

Логи сохраняются в `logs/debug.log`

Уровень логирования настраивается в `settings.py`:

```python
LOGGING = {
    'root': {
        'level': 'DEBUG',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    },
}
```

## 🔄 CORS Configuration

Настройка CORS в `.env`:

```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://example.com
```

## 🐛 Решение проблем

### Ошибка "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### Ошибка базы данных

```bash
python manage.py migrate
```

### Очистить кэш миграций

```bash
python manage.py migrate --reset
```

## 📞 Поддержка

Для вопросов и предложений создавайте issues в репозитории.

## 📄 Лицензия

MIT License - см. LICENSE файл

## 👨‍💻 Автор

Разработано как полнофункциональная система управления электронным журналом для учебных заведений.

---

**Версия:** 1.0.0  
**Последнее обновление:** Март 2026
