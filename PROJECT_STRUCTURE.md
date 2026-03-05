# Структура проекта - Project Structure

```
dnevnik-api/
│
├── dnevnik_project/              # Django проект (основная конфигурация)
│   ├── __init__.py
│   ├── settings.py               # Основные параметры Django
│   ├── urls.py                   # Главный роутер
│   ├── wsgi.py                   # WSGI для production
│   └── asgi.py                   # ASGI для async
│
├── apps/                          # Django приложения
│   │
│   ├── core/                      # Общие модели и утилиты
│   │   ├── models.py              # BaseModel, TimeStampedModel
│   │   ├── permissions.py         # Permission классы
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── tests.py
│   │
│   ├── accounts/                  # Управление пользователями
│   │   ├── models.py              # User, Teacher, Student
│   │   ├── serializers.py         # UserSerializer, etc.
│   │   ├── views.py               # UserViewSet, TokenView
│   │   ├── urls.py                # Маршруты аутентификации
│   │   ├── admin_urls.py          # Маршруты администратора
│   │   ├── admin.py               # Админ панель
│   │   ├── apps.py
│   │   └── migrations/            # Миграции БД
│   │
│   ├── academics/                 # Учебный процесс
│   │   ├── models.py              # Subject, Group, Schedule, Lesson
│   │   ├── serializers.py         # Сериализаторы
│   │   ├── views.py               # ViewSets
│   │   ├── urls.py                # Маршруты
│   │   ├── admin.py               # Админ панель
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── journal/                   # Журнал (посещаемость, оценки)
│   │   ├── models.py              # Attendance, Grade
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── homework/                  # Домашнее задание
│   │   ├── models.py              # Homework, HomeworkMaterial, Submission
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   └── exams/                     # Экзамены
│       ├── models.py              # Exam, ExamResult, ExamQuestion
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       ├── apps.py
│       └── migrations/
│
├── staticfiles/                   # Собранные статические файлы (генерируется)
├── media/                         # Загруженные файлы пользователей
├── logs/                          # Логи приложения (генерируется)
│
├── manage.py                      # Django CLI
├── requirements.txt               # Python зависимости
├── .env                          # Переменные окружения (локальный)
├── .env.example                  # Пример переменных окружения
├── .gitignore                    # Git исключения
│
├── Dockerfile                    # Docker образ для контейнеризации
├── docker-compose.yml            # Docker Compose конфигурация
├── nginx.conf                    # Nginx конфигурация для production
│
├── init_project.sh               # Инициализация проекта (Linux/Mac)
├── init_project.bat              # Инициализация проекта (Windows)
│
├── create_test_data.py           # Скрипт создания тестовых данных
│
├── README.md                     # Основная документация
├── QUICKSTART.md                 # Быстрый старт
├── API_EXAMPLES.md               # Примеры API запросов
├── PRODUCTION.md                 # Гайд для production развертывания
└── PROJECT_STRUCTURE.md          # Этот файл
```

## Описание основных компонентов

### dnevnik_project/

**Главная конфигурация Django проекта**

- `settings.py` - Все параметры проекта (БД, приложения, middleware, etc.)
- `urls.py` - Главный роутер API (подключает все приложения)
- `wsgi.py` - Точка входа для production серверов (Gunicorn)
- `asgi.py` - Для асинхронных операций

### apps/core/

**Общие утилиты и базовые модели**

- `models.py` - Абстрактные классы `TimeStampedModel`, `BaseModel`
- `permissions.py` - Permission классы для role-based access control
- Используется другими приложениями

### apps/accounts/

**Управление пользователями и аутентификацией**

```
Модели:
- User (кастомная модель)
- Teacher (профиль учителя)
- Student (профиль студента)

Endpoints:
- POST /api/v1/auth/login/           - Вход
- GET  /api/v1/auth/users/me/        - Текущий пользователь
- POST /api/v1/auth/users/change_password/  - Смена пароля

Администраторские эндпойнты:
- POST   /api/v1/admin/users/        - Создать пользователя
- GET    /api/v1/admin/users/        - Список пользователей
- PATCH  /api/v1/admin/users/{id}/   - Обновить
- DELETE /api/v1/admin/users/{id}/   - Удалить
```

### apps/academics/

**Учебный процесс**

```
Модели:
- Subject (предмет)
- Group (группа/класс)
- Schedule (расписание)
- Lesson (урок)
- TeacherSubject (связь учителя с предметом)

Endpoints:
- /api/v1/academics/subjects/
- /api/v1/academics/groups/
- /api/v1/academics/schedules/
- /api/v1/academics/lessons/
```

### apps/journal/

**Журнал (посещаемость и оценки)**

```
Модели:
- Attendance (посещаемость)
- Grade (оценка)
- StudentGradeAverage (средняя оценка)

Endpoints:
- /api/v1/journal/attendance/        - Посещаемость
- /api/v1/journal/grades/            - Оценки
- /api/v1/journal/grade-averages/    - Средние оценки
```

### apps/homework/

**Домашнее задание**

```
Модели:
- Homework (домашнее задание)
- HomeworkMaterial (материалы)
- StudentHomeworkSubmission (сдача студента)

Endpoints:
- /api/v1/homework/homeworks/
- /api/v1/homework/materials/
- /api/v1/homework/submissions/
```

### apps/exams/

**Экзамены**

```
Модели:
- Exam (экзамен)
- ExamResult (результат экзамена)
- ExamQuestion (вопрос экзамена)

Endpoints:
- /api/v1/exams/exams/
- /api/v1/exams/results/
- /api/v1/exams/questions/
```

## Архитектурные паттерны

### Models (ORM)

Каждое приложение содержит `models.py` с определением структуры БД.

```python
class MyModel(TimeStampedModel):
    # Наследуется created_at, updated_at
    field1 = models.CharField(...)
```

### Serializers (DRF)

Преобразование моделей в JSON и валидация входных данных.

```python
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = [...]
```

### ViewSets (DRF)

REST эндпойнты с CRUD операциями.

```python
class MyViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    permission_classes = [IsAuthenticated]
```

### URLs (Django)

Регистрация эндпойнтов.

```python
router = DefaultRouter()
router.register(r'mymodels', MyViewSet)
urlpatterns = [path('', include(router.urls))]
```

## Отношения между моделями

```
User (1) ──── (1) Teacher ──── (*) Subject
 │                  │
 │              (*) Schedule
 │                  │
 │              (*) Lesson
 │                  │
 │              (*) Attendance
 │
 └─ (1) Student ──── (1) Group
        │
        ├── (*) Attendance
        ├── (*) Grade
        ├── (*) Homework Submission
        └── (*) Exam Result

Group ──── (*) Subject ──── (*) Lesson
            │                 │
            ├── (*) Homework  │
            └── (*) Exam ─────┘

Homework ──── (*) HomeworkMaterial
     │
     └──── (*) StudentHomeworkSubmission

Exam ──── (*) ExamQuestion
     └──── (*) ExamResult
```

## Процесс разработки

### 1. Создание нового эндпойнта

```
1. Модель:        apps/myapp/models.py
2. Миграция:      python manage.py makemigrations
3. Сериализатор:  apps/myapp/serializers.py
4. ViewSet:       apps/myapp/views.py
5. URL:           apps/myapp/urls.py
6. Admin:         apps/myapp/admin.py
7. Тесты:         apps/myapp/tests.py
8. Миграция:      python manage.py migrate
```

### 2. Добавление поля к существующей модели

```bash
# 1. Обновить модель в models.py
# 2. Создать миграцию
python manage.py makemigrations

# 3. Применить миграцию
python manage.py migrate

# 4. Обновить сериализатор
# 5. Обновить админ панель (опционально)
```

## Использование правильно

### ✅ DO's

- Использовать role-based permissions
- Использовать select_related для ForeignKey
- Использовать prefetch_related для ManyToMany
- Проверять права доступа в ViewSet
- Документировать API эндпойнты
- Писать тесты

### ❌ DON'Ts

- Не использовать N+1 queries
- Не передавать пароли через API
- Не хранить чувствительные данные в логах
- Не забывать про валидацию
- Не создавать глобальные состояния

## Файлы инициализации

### init_project.sh (Linux/Mac)

```bash
bash init_project.sh
```

Автоматически:
- Создает виртуальное окружение
- Устанавливает зависимости
- Применяет миграции
- Создает суперпользователя

### init_project.bat (Windows)

```cmd
init_project.bat
```

То же самое, но для Windows.

## Конфигурационные файлы

- `.env` - Переменные окружения (не коммитится)
- `.env.example` - Пример конфига (коммитится)
- `.gitignore` - Исключения для git
- `requirements.txt` - Python зависимости

## Развертывание

### Development

```bash
python manage.py runserver
```

### Docker

```bash
docker-compose up -d
```

### Production (см. PRODUCTION.md)

- Gunicorn + Nginx
- SSL сертификаты
- Резервное копирование

---

**Версия:** 1.0.0  
**Последнее обновление:** Март 2026
