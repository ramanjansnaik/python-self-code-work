# Production Deployment Guide

This guide covers deploying TestGen to production environments.

## Pre-deployment Checklist

- [ ] Generate a strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database (PostgreSQL)
- [ ] Configure static file serving
- [ ] Set up HTTPS/SSL
- [ ] Configure environment variables
- [ ] Set up logging
- [ ] Configure backup strategy

## Production Settings

### Security Settings

Add to `precostcalc/settings.py` or create `precostcalc/settings_prod.py`:

```python
import os

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# HTTPS/SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/testgen/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## Environment Variables

Create a production `.env` file:

```env
# Django
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=testgen_prod
DB_USER=testgen_user
DB_PASSWORD=strong-database-password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Server Setup (Ubuntu/Debian)

### 1. System Prerequisites

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql nginx supervisor
```

### 2. PostgreSQL Setup

```bash
# Create database and user
sudo -u postgres psql

postgres=# CREATE DATABASE testgen_prod;
postgres=# CREATE USER testgen_user WITH PASSWORD 'strong-password';
postgres=# ALTER ROLE testgen_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE testgen_user SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE testgen_user SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE testgen_prod TO testgen_user;
postgres=# \q
```

### 3. Application Setup

```bash
# Create application directory
sudo mkdir -p /opt/testgen
sudo chown $USER:$USER /opt/testgen
cd /opt/testgen

# Clone repository
git clone <your-repo-url> .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install psycopg2-binary

# Create .env file
nano .env
# (paste production environment variables)

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 4. Gunicorn Setup

Create `/etc/supervisor/conf.d/testgen.conf`:

```ini
[program:testgen]
command=/opt/testgen/venv/bin/gunicorn --workers 3 --bind unix:/opt/testgen/testgen.sock precostcalc.wsgi:application
directory=/opt/testgen
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/testgen/gunicorn.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/testgen
sudo chown www-data:www-data /var/log/testgen

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start testgen
```

### 5. Nginx Setup

Create `/etc/nginx/sites-available/testgen`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 100M;
    
    # Static files
    location /static/ {
        alias /opt/testgen/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /opt/testgen/media/;
    }
    
    # Frontend (React build)
    location / {
        root /opt/testgen/frontend/build;
        try_files $uri /index.html;
    }
    
    # API requests
    location /api/ {
        proxy_pass http://unix:/opt/testgen/testgen.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Admin
    location /admin/ {
        proxy_pass http://unix:/opt/testgen/testgen.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/testgen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 7. Frontend Build

```bash
cd /opt/testgen/frontend
npm install
npm run build
```

## Docker Deployment

### Using Docker Compose

1. Update `docker-compose.yml` for production:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - DB_NAME=testgen_db
      - DB_USER=testgen_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
    depends_on:
      - db
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=testgen_db
      - POSTGRES_USER=testgen_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/prod.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/static
      - media_volume:/media
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

2. Deploy:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring & Maintenance

### Health Checks

Create a health check endpoint in Django:

```python
# Add to testgen/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy'})
```

### Monitoring Tools

- **Application**: Sentry for error tracking
- **Server**: Prometheus + Grafana
- **Uptime**: UptimeRobot or Pingdom
- **Logs**: ELK Stack or CloudWatch

### Backup Strategy

```bash
# Database backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/testgen"
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U testgen_user testgen_prod > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /opt/testgen/media/

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /opt/testgen/backup.sh
```

## Performance Optimization

### 1. Database

```python
# Add to settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### 2. Caching

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. Static Files

Use WhiteNoise or CDN for static files.

## Troubleshooting

### Common Issues

**500 Internal Server Error**
- Check gunicorn logs: `tail -f /var/log/testgen/gunicorn.log`
- Check nginx error log: `sudo tail -f /var/log/nginx/error.log`
- Verify environment variables

**Database Connection Issues**
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database credentials
- Check firewall rules

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check nginx static file configuration
- Verify file permissions

## Scaling

### Horizontal Scaling

1. Use load balancer (nginx, HAProxy)
2. Run multiple gunicorn instances
3. Use Redis for session storage
4. Set up database replication

### Vertical Scaling

1. Increase gunicorn workers
2. Optimize database queries
3. Use caching extensively
4. Optimize static assets

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up firewall (UFW)
- [ ] Configure fail2ban
- [ ] Regular security updates
- [ ] Secure API keys in environment variables
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Limit database user permissions
- [ ] Use strong passwords

## Support

For deployment issues:
- Check application logs
- Review nginx/gunicorn logs
- Verify environment configuration
- Test database connectivity

---

Good luck with your deployment! 🚀
