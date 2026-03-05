# Production Configuration Guide

## Развертывание в Production

### 1. Конфигурация для Production

Обновите файл `.env`:

```env
DEBUG=False
SECRET_KEY=<сгенерируйте_сложный_ключ>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dnevnik_db
DB_USER=postgres
DB_PASSWORD=<сложный_пароль>
DB_HOST=db_server_ip
DB_PORT=5432
```

### 2. Генерация SECRET_KEY

```python
# В Python оболочке
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. Сбор статических файлов

```bash
python manage.py collectstatic --noinput --clear
```

### 4. Миграция БД

```bash
python manage.py migrate --noinput
```

### 5. Запуск с Gunicorn

```bash
# Установка
pip install gunicorn

# Запуск
gunicorn dnevnik_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 120
```

### 6. Использование Systemd сервиса

Создайте `/etc/systemd/system/dnevnik.service`:

```ini
[Unit]
Description=Dnevnik API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/home/user/dnevnik-api
Environment="PATH=/home/user/dnevnik-api/venv/bin"
ExecStart=/home/user/dnevnik-api/venv/bin/gunicorn \
    dnevnik_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl start dnevnik
sudo systemctl enable dnevnik
```

### 7. Nginx конфигурация

Создайте `/etc/nginx/sites-available/dnevnik`:

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Редирект на HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL сертификаты
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    client_max_body_size 100M;
    
    # Статические файлы
    location /static/ {
        alias /home/user/dnevnik-api/staticfiles/;
        expires 30d;
    }
    
    # Медиа файлы
    location /media/ {
        alias /home/user/dnevnik-api/media/;
        expires 7d;
    }
    
    # API запросы
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Таймауты
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Активация:

```bash
sudo ln -s /etc/nginx/sites-available/dnevnik /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL сертификат (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9. Автоматическое обновление сертификата

```bash
# Тест
sudo certbot renew --dry-run

# Автоматическое продление
sudo systemctl enable certbot.timer
```

### 10. Мониторинг логов

```bash
# Логи Gunicorn
tail -f /var/log/dnevnik.log

# Логи Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Логи Django
tail -f /home/user/dnevnik-api/logs/debug.log
```

### 11. Резервное копирование БД

```bash
#!/bin/bash
# backup_db.sh

BACKUP_DIR="/backups/dnevnik"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="dnevnik_db"

mkdir -p $BACKUP_DIR

pg_dump -U postgres $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

Добавьте в crontab:

```bash
0 2 * * * /path/to/backup_db.sh
```

### 12. Docker развертывание

```bash
docker-compose -f docker-compose.yml up -d
```

### 13. Оптимизация PostgreSQL

```sql
-- Увеличение памяти
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET max_wal_size = '1GB';

-- Перезагрузка
SELECT pg_reload_conf();
```

### 14. Мониторинг производительности

```bash
# Установка New Relic (опционально)
pip install newrelic

# Запуск с мониторингом
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program \
    gunicorn dnevnik_project.wsgi:application
```

### 15. Безопасность

```python
# settings.py для production

# HTTPS only
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# Отключить DEBUG
DEBUG = False

# Установить ALLOWED_HOSTS
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

---

Последнее обновление: март 2026
