# Развертывание на DigitalOcean App Platform с DigitalOcean Spaces

Это руководство поможет вам развернуть ваше Django-приложение на DigitalOcean App Platform с использованием DigitalOcean Spaces для статических и медиа файлов.

## Преимущества использования DigitalOcean Spaces

- **CDN**: Автоматическое распространение контента через CDN для быстрой загрузки по всему миру
- **Масштабируемость**: Неограниченное хранилище для файлов
- **Производительность**: Разгрузка сервера приложений от раздачи статики
- **Надежность**: Репликация данных и высокая доступность
- **Стоимость**: $5/месяц за 250GB хранилища + 1TB трафика

## Предварительные требования

1. Аккаунт на [DigitalOcean](https://www.digitalocean.com/)
2. Ваш репозиторий на GitHub (IbroIT/e-library-front)

## Шаг 1: Создание DigitalOcean Spaces

### 1.1 Создание Space

1. Войдите в [DigitalOcean Dashboard](https://cloud.digitalocean.com/)
2. В левом меню выберите **Spaces Object Storage**
3. Нажмите **Create a Space**
4. Настройте параметры:
   - **Datacenter Region**: Frankfurt (fra1) - ближе к вашим пользователям
   - **Enable CDN**: ✅ Включите CDN (важно для производительности!)
   - **Space Name**: `e-library-media` (или любое уникальное имя)
   - **File Listing**: Выберите **Restrict File Listing** (безопасность)
   - **Project**: Выберите ваш проект или оставьте по умолчанию
5. Нажмите **Create a Space**

### 1.2 Получение ключей доступа

1. В верхнем меню выберите **API**
2. Перейдите на вкладку **Spaces access keys**
3. Нажмите **Generate New Key**
4. Дайте ключу название: `e-library-backend`
5. **ВАЖНО**: Сохраните **Access Key** и **Secret Key** - секретный ключ показывается только один раз!

Пример:
```
Access Key: DO00ABC123XYZ789
Secret Key: supersecretkey123456789abcdefghijklmnop
```

### 1.3 Настройка CORS для Space

1. Откройте ваш Space
2. Перейдите на вкладку **Settings**
3. В разделе **CORS Configurations** нажмите **Add**
4. Добавьте следующую конфигурацию:

```
Origin: https://su-e-library.vercel.app
Allowed Methods: GET, PUT, POST, DELETE, HEAD
Allowed Headers: *
```

Добавьте еще одну для вашего основного домена:
```
Origin: https://su-library.com
Allowed Methods: GET, PUT, POST, DELETE, HEAD
Allowed Headers: *
```

## Шаг 2: Развертывание приложения на App Platform

### 2.1 Создание приложения

1. Перейдите в раздел **Apps** в левом меню
2. Нажмите **Create App**
3. Выберите **GitHub** в качестве источника
4. Авторизуйте DigitalOcean для доступа к вашим репозиториям
5. Выберите репозиторий: `IbroIT/e-library-front`
6. Выберите ветку: `main`
7. Укажите **Source Directory**: `/backend`
8. Нажмите **Next**

### 2.2 Настройка сервиса

1. DigitalOcean автоматически определит Python приложение
2. Настройте следующие параметры:
   - **Resource Type**: Web Service
   - **Environment**: Python
   - **HTTP Port**: 8000
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
     ```
   - **Run Command**:
     ```bash
     gunicorn backend.wsgi --log-file -
     ```

### 2.3 Добавление базы данных

1. Нажмите **Add Resource** → **Database**
2. Выберите **PostgreSQL** версии 12 или выше
3. Выберите размер: **Basic** ($15/месяц)
4. Нажмите **Create and Attach**

### 2.4 Настройка переменных окружения

Добавьте следующие переменные окружения:

#### Обязательные переменные:

```env
# Django секретный ключ (сгенерируйте новый!)
SECRET_KEY=your-secret-key-here

# Отключаем debug в продакшене
DEBUG=False

# Разрешенные хосты (будет автоматически подставлен домен)
ALLOWED_HOSTS=${APP_DOMAIN},${_self.ONDIGITALOCEAN_APP_URL}

# CORS origins для фронтенда
CORS_ALLOWED_ORIGINS=https://su-e-library.vercel.app,https://su-library.com

# База данных (автоматически из созданной БД)
DATABASE_URL=${db.DATABASE_URL}

# Django settings модуль
DJANGO_SETTINGS_MODULE=backend.settings
```

#### Переменные для DigitalOcean Spaces:

```env
# Включаем использование Spaces
USE_SPACES=True

# Ваши ключи доступа из шага 1.2
AWS_ACCESS_KEY_ID=DO00ABC123XYZ789
AWS_SECRET_ACCESS_KEY=supersecretkey123456789abcdefghijklmnop

# Имя вашего Space
AWS_STORAGE_BUCKET_NAME=e-library-media

# Endpoint URL для Frankfurt
AWS_S3_ENDPOINT_URL=https://fra1.digitaloceanspaces.com

# Регион
AWS_S3_REGION_NAME=fra1

# CDN домен (важно для производительности!)
AWS_S3_CUSTOM_DOMAIN=e-library-media.fra1.cdn.digitaloceanspaces.com
```

**Важно**: 
- Замените значения `AWS_ACCESS_KEY_ID` и `AWS_SECRET_ACCESS_KEY` на ваши реальные ключи
- Отметьте эти переменные как **Encrypted** (секретные)
- CDN домен имеет формат: `ваш-space-name.регион.cdn.digitaloceanspaces.com`

**Генерация SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2.5 Выбор региона и плана

1. Выберите регион: **Frankfurt** (тот же, что и для Space)
2. Выберите план:
   - **Basic**: $5/месяц (512MB RAM, 1 vCPU)
   - **Professional**: от $12/месяц (для production с большой нагрузкой)

### 2.6 Запуск развертывания

1. Проверьте все настройки
2. Нажмите **Create Resources**
3. Дождитесь завершения развертывания (5-10 минут)

## Шаг 3: Проверка работы

### 3.1 Получение URL приложения

После успешного развертывания вы получите URL:
```
https://e-library-backend-xxxxx.ondigitalocean.app
```

### 3.2 Создание суперпользователя

1. Перейдите в **Apps** → ваше приложение
2. Откройте вкладку **Console**
3. Выполните команду:
```bash
python manage.py createsuperuser
```

### 3.3 Загрузка существующих медиа файлов в Spaces

Если у вас уже есть медиа файлы локально, загрузите их в Space:

#### Вариант 1: Через веб-интерфейс
1. Откройте ваш Space
2. Создайте папку `media`
3. Перетащите файлы в папку

#### Вариант 2: Через AWS CLI (s3cmd)

Установите s3cmd:
```bash
pip install s3cmd
```

Настройте s3cmd:
```bash
s3cmd --configure
```

Введите:
- Access Key: ваш ключ из шага 1.2
- Secret Key: ваш секретный ключ
- Default Region: fra1
- S3 Endpoint: fra1.digitaloceanspaces.com
- DNS-style bucket: %(bucket)s.fra1.digitaloceanspaces.com

Загрузите файлы:
```bash
s3cmd sync ./media/ s3://e-library-media/media/ --acl-public
```

### 3.4 Проверка доступа к файлам

Проверьте URL медиа файлов:
```
https://e-library-media.fra1.cdn.digitaloceanspaces.com/media/books/covers/test.jpg
```

Проверьте API:
```
https://ваш-домен.ondigitalocean.app/api/books/
```

## Шаг 4: Настройка домена (опционально)

### 4.1 Добавление домена к приложению

1. В настройках приложения перейдите в **Settings** → **Domains**
2. Нажмите **Add Domain**
3. Введите ваш домен (например, `api.su-library.com`)
4. Добавьте CNAME запись у вашего DNS провайдера:
```
CNAME api e-library-backend-xxxxx.ondigitalocean.app
```

### 4.2 Пользовательский домен для CDN (опционально)

Вы можете настроить пользовательский домен для CDN:

1. Откройте ваш Space → **Settings**
2. В разделе **Custom Domain** нажмите **Add a Domain**
3. Введите домен: `cdn.su-library.com`
4. Добавьте CNAME запись:
```
CNAME cdn e-library-media.fra1.cdn.digitaloceanspaces.com
```
5. Обновите переменную `AWS_S3_CUSTOM_DOMAIN`:
```
AWS_S3_CUSTOM_DOMAIN=cdn.su-library.com
```

## Мониторинг и обслуживание

### Просмотр логов

1. Перейдите в ваше приложение
2. Откройте вкладку **Runtime Logs**

### Просмотр метрик

В разделе **Insights**:
- CPU и память
- Количество запросов
- Время отклика
- Использование базы данных

### Просмотр использования Spaces

1. Откройте ваш Space
2. Вкладка **Settings** → **Usage**
- Объем хранилища
- Количество объектов
- Bandwidth (трафик)

## Оптимизация производительности

### 1. Настройка Cache-Control

Настройки кеширования уже включены в `settings.py`:
```python
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1 день
}
```

### 2. Сжатие изображений

Для оптимизации размера изображений используйте Pillow:
```python
# В вашем коде при загрузке изображений
from PIL import Image
from io import BytesIO

def optimize_image(image_file):
    img = Image.open(image_file)
    output = BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)
    return output
```

### 3. Использование разных папок для статики и медиа

Можно настроить отдельные пути в Spaces. Обновите `settings.py`:

```python
# Разные пути для статики и медиа
AWS_LOCATION_STATIC = 'static'
AWS_LOCATION_MEDIA = 'media'

# Custom storage classes
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

# В settings.py
STATICFILES_STORAGE = 'backend.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'backend.storage_backends.MediaStorage'
```

## Стоимость

Примерная стоимость:

- **App Platform (Basic)**: $5/месяц
- **PostgreSQL (Basic)**: $15/месяц
- **Spaces**: $5/месяц (250GB + 1TB трафика)
- **Дополнительный трафик**: $0.01/GB после первого 1TB

**Итого**: ~$25/месяц

## Резервное копирование

### База данных

DigitalOcean делает автоматические ежедневные бэкапы PostgreSQL.

### Spaces

Включите versioning для защиты от случайного удаления:
1. Откройте Space → **Settings**
2. Включите **Versioning**

Для дополнительных бэкапов используйте:
```bash
s3cmd sync s3://e-library-media/ ./backup/ --skip-existing
```

## Troubleshooting

### Файлы не загружаются в Spaces

1. Проверьте ключи доступа
2. Убедитесь, что переменная `USE_SPACES=True`
3. Проверьте CORS настройки в Space
4. Проверьте логи: `Access denied` или `403` ошибки

### Файлы не отображаются на фронтенде

1. Проверьте CORS настройки
2. Убедитесь, что CDN домен правильный
3. Проверьте публичность файлов: `AWS_DEFAULT_ACL = 'public-read'`
4. Откройте DevTools браузера и проверьте URL файлов

### Статические файлы Django Admin не работают

Выполните collectstatic вручную:
```bash
python manage.py collectstatic --noinput
```

### Большие расходы на трафик

1. Убедитесь, что CDN включен
2. Настройте более длительный Cache-Control
3. Оптимизируйте размеры изображений
4. Используйте современные форматы (WebP)

## Миграция с Heroku

Если вы переходите с Heroku:

1. Экспортируйте данные из Heroku PostgreSQL
2. Импортируйте в DigitalOcean PostgreSQL
3. Скачайте медиа файлы из Heroku
4. Загрузите в DigitalOcean Spaces
5. Обновите DNS на новый домен

## Полезные команды

### Проверка подключения к Spaces
```python
python manage.py shell

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Тест записи
path = default_storage.save('test.txt', ContentFile(b'Hello World'))
print(f"Saved: {path}")
print(f"URL: {default_storage.url(path)}")

# Тест чтения
content = default_storage.open('test.txt').read()
print(f"Content: {content}")

# Удаление теста
default_storage.delete('test.txt')
```

### Массовая загрузка файлов
```python
python manage.py shell

from main.models import Book
from django.core.files import File

# Обновить все книги с новыми URL
for book in Book.objects.all():
    if book.pdf_file:
        print(f"Updated: {book.title} - {book.pdf_file.url}")
```

## Полезные ссылки

- [DigitalOcean App Platform Docs](https://docs.digitalocean.com/products/app-platform/)
- [DigitalOcean Spaces Docs](https://docs.digitalocean.com/products/spaces/)
- [django-storages Documentation](https://django-storages.readthedocs.io/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Поддержка

При возникновении проблем:
1. Проверьте логи приложения и Spaces
2. Посетите [Community Forum](https://www.digitalocean.com/community/)
3. Откройте [Support Ticket](https://cloud.digitalocean.com/support/tickets)
