# Render Deployment Guide

## Автоматическое развертывание на Render

### Шаг 1: Подготовка репозитория

Проект уже готов к развертыванию на Render. Все изменения закоммичены и отправлены в GitHub.

### Шаг 2: Создание Web Service на Render

1. Перейдите на [Render Dashboard](https://dashboard.render.com/)
2. Нажмите **"New +"** → **"Web Service"**
3. Подключите GitHub репозиторий: `sibcoww/dnevnik-api`
4. Настройте параметры:

   - **Name**: `dnevnik-api`
   - **Region**: выберите ближайший регион
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     python manage.py migrate && python manage.py collectstatic --noinput && gunicorn dnevnik_project.wsgi:application
     ```

### Шаг 3: Создание PostgreSQL базы данных

1. В Render Dashboard нажмите **"New +"** → **"PostgreSQL"**
2. Настройте:
   - **Name**: `dnevnik-db`
   - **Database**: `dnevnik_db`
   - **User**: `dnevnik_user`
   - **Region**: тот же, что и Web Service
   - **Plan**: выберите подходящий план

3. После создания скопируйте **Internal Database URL**

### Шаг 4: Настройка переменных окружения

В настройках Web Service добавьте Environment Variables:

```bash
# Django Settings
SECRET_KEY=<generate-random-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# Database (из Internal Database URL PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database

# CORS (добавьте ваши домены)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-app-name.onrender.com

# JWT (опционально, если хотите изменить время жизни токенов)
# SIMPLE_JWT_ALGORITHM=HS256
```

### Шаг 5: Deploy

1. Нажмите **"Create Web Service"**
2. Render автоматически:
   - Установит зависимости из `requirements.txt`
   - Выполнит миграции БД
   - Соберет статические файлы
   - Запустит Gunicorn сервер

### Шаг 6: Создание суперпользователя

После успешного деплоя:

1. В Render Dashboard перейдите в ваш Web Service
2. Откройте **Shell** (вкладка Shell)
3. Выполните команду:
   ```bash
   python manage.py createsuperuser
   ```
4. Введите данные администратора

## Доступ к API

После развертывания API будет доступен по адресу:

- **API Root**: `https://your-app-name.onrender.com/api/v1/`
- **Swagger Docs**: `https://your-app-name.onrender.com/api/docs/`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`
- **System Admin API**: `https://your-app-name.onrender.com/api/v1/sysadmin/`

## Важные замечания

### 1. URL Namespace изменен

⚠️ **ВАЖНО**: Административный API namespace изменен с `/api/v1/admin/` на `/api/v1/sysadmin/`

Это сделано для устранения конфликта с встроенной Django admin панелью.

**Старый URL** (больше не работает):
```
POST /api/v1/admin/users/
```

**Новый URL** (используйте этот):
```
POST /api/v1/sysadmin/users/
```

### 2. Static Files

WhiteNoise автоматически обслуживает статические файлы. Никакие дополнительные настройки не требуются.

### 3. Database Migrations

Миграции выполняются автоматически при каждом деплое через команду в `startCommand`.

### 4. Monitoring

Render предоставляет встроенный мониторинг:
- Логи доступны в разделе **Logs**
- Метрики в разделе **Metrics**

## Локальная разработка

Для локальной разработки используйте `.env` файл:

```bash
# .env
DEBUG=True
SECRET_KEY=your-local-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Для PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dnevnik_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Для SQLite (если не хотите устанавливать PostgreSQL)
# DB_ENGINE=django.db.backends.sqlite3
```

## Обновление проекта

Для обновления на Render:

```bash
git add .
git commit -m "your changes"
git push origin main
```

Render автоматически обнаружит изменения и выполнит повторное развертывание.

## Troubleshooting

### Ошибка миграций

Если миграции не применились:
1. Откройте Shell в Render
2. Выполните вручную:
   ```bash
   python manage.py migrate
   ```

### Статические файлы не загружаются

Проверьте, что WhiteNoise middleware добавлен в `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Должен быть вторым
    ...
]
```

### Ошибка подключения к БД

Убедитесь, что `DATABASE_URL` правильно настроен в Environment Variables.

## Дополнительная информация

- [Render Python Documentation](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

**Проект готов к production!** 🚀
