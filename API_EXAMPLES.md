# API Examples - Примеры использования API

Документ с примерами запросов к API Dnevnik

## Содержание

- [Аутентификация](#аутентификация)
- [Управление пользователями](#управление-пользователями)
- [Предметы](#предметы)
- [Группы](#группы)
- [Расписание](#расписание)
- [Уроки](#уроки)
- [Посещаемость](#посещаемость)
- [Оценки](#оценки)
- [Домашнее задание](#домашнее-задание)
- [Экзамены](#экзамены)

---

## Аутентификация

### Вход (получить токены)

**Request:**
```bash
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "teacher1",
  "password": "teacher123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 2,
    "username": "teacher1",
    "first_name": "Иван",
    "last_name": "Сидоров",
    "email": "teacher1@example.com",
    "role": "teacher"
  }
}
```

### Обновить access токен

**Request:**
```bash
POST /api/v1/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Получить текущего пользователя

**Request:**
```bash
GET /api/v1/auth/users/me/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 2,
  "username": "teacher1",
  "first_name": "Иван",
  "last_name": "Сидоров",
  "full_name": "Иван Сидоров",
  "email": "teacher1@example.com",
  "role": "teacher",
  "is_active": true,
  "date_joined": "2024-03-06T10:00:00Z"
}
```

---

## Управление пользователями

### Создать пользователя (администратор)

**Request:**
```bash
POST /api/v1/admin/users/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "username": "newstudent",
  "password": "SecurePass123",
  "first_name": "Петр",
  "last_name": "Федоров",
  "email": "petr@example.com",
  "role": "student"
}
```

**Response (201 Created):**
```json
{
  "id": 10,
  "username": "newstudent",
  "first_name": "Петр",
  "last_name": "Федоров",
  "full_name": "Петр Федоров",
  "email": "petr@example.com",
  "role": "student",
  "is_active": true,
  "date_joined": "2024-03-06T11:00:00Z"
}
```

### Обновить пользователя (администратор)

**Request:**
```bash
PATCH /api/v1/admin/users/10/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "first_name": "Пётр",
  "email": "petr_new@example.com"
}
```

### Удалить пользователя (администратор)

**Request:**
```bash
DELETE /api/v1/admin/users/10/
Authorization: Bearer <admin_token>
```

**Response (204 No Content)**

### Изменить пароль

**Request:**
```bash
POST /api/v1/auth/users/change_password/
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "oldpass123",
  "new_password": "newpass123"
}
```

---

## Предметы

### Список предметов

**Request:**
```bash
GET /api/v1/academics/subjects/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Математика",
    "description": "Основной курс математики"
  },
  {
    "id": 2,
    "name": "Физика",
    "description": "Физика для 10 класса"
  }
]
```

### Поиск предметов

**Request:**
```bash
GET /api/v1/academics/subjects/?search=математика
Authorization: Bearer <token>
```

---

## Группы

### Создать группу (академический офис)

**Request:**
```bash
POST /api/v1/academics/groups/
Authorization: Bearer <academic_office_token>
Content-Type: application/json

{
  "name": "10-B",
  "academic_year": "2024-2025",
  "description": "Десятый класс, группа Б"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "name": "10-B",
  "academic_year": "2024-2025",
  "description": "Десятый класс, группа Б",
  "created_at": "2024-03-06T10:00:00Z",
  "updated_at": "2024-03-06T10:00:00Z"
}
```

### Список групп

**Request:**
```bash
GET /api/v1/academics/groups/
Authorization: Bearer <token>
```

### Получить группу

**Request:**
```bash
GET /api/v1/academics/groups/1/
Authorization: Bearer <token>
```

---

## Расписание

### Создать расписание (академический офис)

**Request:**
```bash
POST /api/v1/academics/schedules/
Authorization: Bearer <academic_office_token>
Content-Type: application/json

{
  "group": 1,
  "subject": 1,
  "teacher": 1,
  "weekday": 0,
  "start_time": "09:00:00",
  "end_time": "10:00:00",
  "room": "101"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "group": 1,
  "group_name": "10-A",
  "subject": 1,
  "subject_name": "Математика",
  "teacher": 1,
  "teacher_name": "Иван Сидоров",
  "weekday": 0,
  "weekday_display": "Monday",
  "start_time": "09:00:00",
  "end_time": "10:00:00",
  "room": "101",
  "created_at": "2024-03-06T10:00:00Z",
  "updated_at": "2024-03-06T10:00:00Z"
}
```

### Получить расписание по группе

**Request:**
```bash
GET /api/v1/academics/schedules/by_group/?group_id=1
Authorization: Bearer <token>
```

### Получить расписание по учителю

**Request:**
```bash
GET /api/v1/academics/schedules/by_teacher/?teacher_id=1
Authorization: Bearer <token>
```

---

## Уроки

### Создать урок (учитель)

**Request:**
```bash
POST /api/v1/academics/lessons/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "schedule": 1,
  "date": "2024-03-07",
  "topic": "Производные функций",
  "notes": "Сложные производные"
}
```

### Уроки на сегодня

**Request:**
```bash
GET /api/v1/academics/lessons/today/
Authorization: Bearer <token>
```

### Предстоящие уроки

**Request:**
```bash
GET /api/v1/academics/lessons/upcoming/?days=14
Authorization: Bearer <token>
```

### Уроки по группе

**Request:**
```bash
GET /api/v1/academics/lessons/by_group/?group_id=1
Authorization: Bearer <token>
```

---

## Посещаемость

### Создать запись посещаемости (учитель)

**Request:**
```bash
POST /api/v1/journal/attendance/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "lesson": 1,
  "student": 1,
  "status": "present",
  "comment": ""
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "lesson": 1,
  "lesson_info": {...},
  "student": 1,
  "student_name": "Студент1 Иванов1",
  "status": "present",
  "comment": "",
  "created_at": "2024-03-06T10:00:00Z",
  "updated_at": "2024-03-06T10:00:00Z"
}
```

### Массовое создание посещаемости

**Request:**
```bash
POST /api/v1/journal/attendance/bulk_create/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "lesson_id": 1,
  "students_data": [
    {
      "student_id": 1,
      "status": "present",
      "comment": ""
    },
    {
      "student_id": 2,
      "status": "absent",
      "comment": "Болеет"
    },
    {
      "student_id": 3,
      "status": "late",
      "comment": ""
    }
  ]
}
```

### Посещаемость студента

**Request:**
```bash
GET /api/v1/journal/attendance/by_student/?student_id=1
Authorization: Bearer <token>
```

### Статистика посещаемости

**Request:**
```bash
GET /api/v1/journal/attendance/statistics/?student_id=1
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "total_lessons": 20,
  "present": 18,
  "absent": 1,
  "late": 1,
  "excused_absence": 0,
  "attendance_percentage": 95.0
}
```

---

## Оценки

### Создать оценку (учитель)

**Request:**
```bash
POST /api/v1/journal/grades/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "student": 1,
  "subject": 1,
  "teacher": 1,
  "value": 5,
  "grade_type": "test",
  "comment": "Отличная работа"
}
```

### Оценки студента

**Request:**
```bash
GET /api/v1/journal/grades/by_student/?student_id=1
Authorization: Bearer <token>
```

### Средняя оценка по предмету

**Request:**
```bash
GET /api/v1/journal/grades/average_by_student_subject/?student_id=1&subject_id=1
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "student_id": 1,
  "subject_id": 1,
  "average": 4.6,
  "count": 5
}
```

---

## Домашнее задание

### Создать домашнее задание (учитель)

**Request:**
```bash
POST /api/v1/homework/homeworks/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "subject": 1,
  "teacher": 1,
  "group": 1,
  "title": "Решить задачи из учебника",
  "description": "Параграф 15, задачи 1-20",
  "deadline": "2024-03-10T23:59:59Z",
  "status": "published"
}
```

### Добавить материал к домашнему заданию (учитель)

**Request:**
```bash
POST /api/v1/homework/materials/
Authorization: Bearer <teacher_token>
Content-Type: multipart/form-data

{
  "homework": 1,
  "title": "Решение примеров",
  "description": "Инструкции по решению",
  "file": <file_data>
}
```

### Сдать домашнее задание (студент)

**Request:**
```bash
POST /api/v1/homework/submissions/1/submit/
Authorization: Bearer <student_token>
Content-Type: multipart/form-data

{
  "submission_text": "Вот мое решение...",
  "submission_file": <file_data>
}
```

### Мои сдачи домашних заданий (студент)

**Request:**
```bash
GET /api/v1/homework/submissions/my_submissions/
Authorization: Bearer <student_token>
```

### Ожидающие проверки (учитель)

**Request:**
```bash
GET /api/v1/homework/submissions/pending/
Authorization: Bearer <teacher_token>
```

### Оценить домашнее задание (учитель)

**Request:**
```bash
PATCH /api/v1/homework/submissions/1/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "grade": 5,
  "feedback": "Отличная работа!",
  "status": "graded"
}
```

---

## Экзамены

### Создать экзамен (учитель)

**Request:**
```bash
POST /api/v1/exams/exams/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "subject": 1,
  "teacher": 1,
  "group": 1,
  "date": "2024-03-20T10:00:00Z",
  "duration_minutes": 120,
  "location": "Аудитория 201",
  "description": "Итоговый экзамен по математике",
  "status": "planned"
}
```

### Начать экзамен

**Request:**
```bash
POST /api/v1/exams/exams/1/start/
Authorization: Bearer <teacher_token>
```

### Завершить экзамен

**Request:**
```bash
POST /api/v1/exams/exams/1/complete/
Authorization: Bearer <teacher_token>
```

### Создать результат экзамена (учитель)

**Request:**
```bash
POST /api/v1/exams/results/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "exam": 1,
  "student": 1,
  "grade": 5,
  "comment": "Хорошая подготовка",
  "points_earned": 95,
  "points_total": 100
}
```

### Мои результаты экзаменов (студент)

**Request:**
```bash
GET /api/v1/exams/results/my_results/
Authorization: Bearer <student_token>
```

### Результаты по экзамену

**Request:**
```bash
GET /api/v1/exams/results/by_exam/?exam_id=1
Authorization: Bearer <token>
```

### Статистика экзамена

**Request:**
```bash
GET /api/v1/exams/results/statistics/?exam_id=1
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "total_students": 25,
  "average_grade": 4.2,
  "min_grade": 3,
  "max_grade": 5
}
```

---

## Общие параметры запросов

### Фильтрация

Все list endpoints поддерживают фильтрацию:

```bash
# По полю
GET /api/v1/academics/groups/?academic_year=2024-2025

# Несколько фильтров
GET /api/v1/journal/grades/?student=1&subject=1
```

### Поиск

Endpoints с поддержкой поиска используют параметр `search`:

```bash
GET /api/v1/academics/subjects/?search=математика
```

### Сортировка

Используйте параметр `ordering`:

```bash
# По возрастанию
GET /api/v1/journal/grades/?ordering=value

# По убыванию
GET /api/v1/journal/grades/?ordering=-value
```

### Пагинация

```bash
# Страница 2, 20 результатов на странице (по умолчанию)
GET /api/v1/academics/groups/?page=2
```

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | OK - Успешный запрос |
| 201 | Created - Ресурс создан |
| 204 | No Content - Успешно удалено |
| 400 | Bad Request - Неверный запрос |
| 401 | Unauthorized - Не авторизирован |
| 403 | Forbidden - Нет доступа |
| 404 | Not Found - Ресурс не найден |
| 500 | Internal Server Error - Ошибка сервера |

---

## Заголовки

Все запросы должны содержать:

```
Authorization: Bearer <access_token>
Content-Type: application/json  (для POST, PATCH, PUT)
```

---

Последнее обновление: март 2026
