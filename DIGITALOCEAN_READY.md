# ✅ Настройка DigitalOcean для E-Library завершена!

## ✅ Что настроено:

### 1. ✅ DigitalOcean Spaces
- **Space**: `su-library`
- **Регион**: Bangalore (blr1)
- **CDN**: Включен
- **Endpoint**: https://blr1.digitaloceanspaces.com
- **CDN URL**: https://su-library.blr1.cdn.digitaloceanspaces.com

### 2. ✅ Backend настроен
- `django-storages` и `boto3` добавлены в requirements.txt
- `settings.py` настроен:
  - **Статические файлы** (CSS/JS админки): локально через Whitenoise
  - **Медиа файлы** (загрузки пользователей): в DigitalOcean Spaces
- Создан `storage_backends.py` с кастомными классами хранения
- Создан скрипт тестирования `test_spaces.py`
- Все тесты подключения пройдены успешно! ✅

### 3. ✅ Конфигурационные файлы
- `.do/app.yaml` - конфигурация для App Platform
- `.env.example` - шаблон переменных окружения
- `.env` - локальные настройки (уже с вашими ключами)

## Следующие шаги для деплоя:

### Шаг 1: Настройте CORS в Space (обязательно!)

1. Откройте https://cloud.digitalocean.com/spaces
2. Выберите Space `su-library`
3. Перейдите в **Settings** → **CORS Configurations**
4. Нажмите **Add CORS Configuration**
5. Добавьте:

```
Origin: https://su-e-library.vercel.app
Allowed Methods: GET, PUT, POST, DELETE, HEAD
Allowed Headers: *
```

И еще одну для основного домена:
```
Origin: https://su-library.com
Allowed Methods: GET, PUT, POST, DELETE, HEAD
Allowed Headers: *
```

### Шаг 2: Разверните на DigitalOcean App Platform

#### Вариант А: Через веб-интерфейс

1. Перейдите на https://cloud.digitalocean.com/apps
2. Нажмите **Create App**
3. Выберите GitHub → репозиторий `IbroIT/e-library-front`
4. Ветка: `main`, Source Directory: `/backend`
5. **Next** → автоматически определит Python

**Настройки сборки:**
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
- Run Command: `gunicorn backend.wsgi --log-file -`
- HTTP Port: `8000`

6. **Add Resource** → **Database** → PostgreSQL 12+

7. **Add Environment Variables** (из файла `.do/app.yaml`):

```env
SECRET_KEY=<сгенерируйте новый ключ>
DEBUG=False
ALLOWED_HOSTS=${APP_DOMAIN},${_self.ONDIGITALOCEAN_APP_URL}
CORS_ALLOWED_ORIGINS=https://su-e-library.vercel.app,https://su-library.com
DATABASE_URL=${db.DATABASE_URL}
DJANGO_SETTINGS_MODULE=backend.settings

USE_SPACES=True
AWS_ACCESS_KEY_ID=DO801328JW7UKUFKDWJJ
AWS_SECRET_ACCESS_KEY=MeSNvR1wHHPs8CLI1f0aaNhYjxLnQ7YRyS+QeHDDSZs
AWS_STORAGE_BUCKET_NAME=su-library
AWS_S3_ENDPOINT_URL=https://blr1.digitaloceanspaces.com
AWS_S3_REGION_NAME=blr1
AWS_S3_CUSTOM_DOMAIN=su-library.blr1.cdn.digitaloceanspaces.com
```

⚠️ **Важно**: Отметьте `SECRET_KEY`, `AWS_ACCESS_KEY_ID` и `AWS_SECRET_ACCESS_KEY` как **Encrypted**!

**Генерация SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

8. Выберите регион: **Bangalore** (близко к вашему Space)
9. План: **Basic** ($5/месяц)
10. **Create Resources**

#### Вариант Б: Через doctl CLI

```bash
# Установите doctl и авторизуйтесь
doctl auth init

# Разверните из конфига
cd backend
doctl apps create --spec .do/app.yaml

# Следите за деплоем
doctl apps list
doctl apps logs <app-id> --follow
```

### Шаг 3: После развертывания

1. **Создайте суперпользователя:**
   - В App Platform → Console:
   ```bash
   python manage.py createsuperuser
   ```

2. **Загрузите существующие медиа файлы:**
   ```bash
   # Установите s3cmd
   pip install s3cmd
   
   # Настройте
   s3cmd --configure
   # Access Key: DO801328JW7UKUFKDWJJ
   # Secret Key: MeSNvR1wHHPs8CLI1f0aaNhYjxLnQ7YRyS+QeHDDSZs
   # Region: blr1
   # Endpoint: blr1.digitaloceanspaces.com
   
   # Загрузите файлы
   s3cmd sync ./media/ s3://su-library/media/ --acl-public
   ```

3. **Обновите URL на фронтенде:**
   - Замените URL бэкенда в `e-library-front` на новый:
   - `https://ваше-приложение.ondigitalocean.app`

4. **Проверьте работу:**
   - API: `https://ваш-домен/api/books/`
   - Admin: `https://ваш-домен/admin/`
   - Медиа файлы: должны загружаться с `su-library.blr1.cdn.digitaloceanspaces.com`

## Тестирование локально

Вы можете протестировать подключение к Spaces локально:

```bash
cd backend

# Убедитесь что USE_SPACES=True в .env
python test_spaces.py

# Запустите сервер
python manage.py runserver

# Загрузите тестовый файл через админку и проверьте URL
```

## Стоимость

- **App Platform (Basic)**: $5/месяц
- **PostgreSQL (Basic)**: $15/месяц
- **Spaces**: $5/месяц (250GB + 1TB трафика)

**Итого**: ~$25/месяц

## Документация

- 📖 [SPACES_SETUP.md](./SPACES_SETUP.md) - быстрая настройка Spaces
- 📖 [DIGITALOCEAN_DEPLOY.md](./DIGITALOCEAN_DEPLOY.md) - полное руководство по развертыванию
- 🔧 [test_spaces.py](./test_spaces.py) - скрипт тестирования подключения

## Поддержка

Если возникнут проблемы:
1. Проверьте логи: App Platform → Runtime Logs
2. Убедитесь что CORS настроен в Space
3. Проверьте переменные окружения
4. Запустите `test_spaces.py` для диагностики

---

**Готово к деплою! 🚀**
