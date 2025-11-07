# Деплой Django приложения на Heroku

## Подготовка к деплою завершена ✓

### Созданные файлы:
1. **requirements.txt** - зависимости проекта
2. **Procfile** - команда запуска для Heroku
3. **runtime.txt** - версия Python
4. **.gitignore** - исключение ненужных файлов
5. **.env.example** - пример переменных окружения

### Обновлено:
- **settings.py** - настройки для production (переменные окружения, PostgreSQL, whitenoise, безопасность)

## Инструкция по деплою:

### 1. Установите Heroku CLI
```bash
# Скачайте и установите с https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Войдите в Heroku
```bash
heroku login
```

### 3. Создайте приложение на Heroku
```bash
cd backend
heroku create your-app-name
```

### 4. Добавьте PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Установите переменные окружения
```bash
# Создайте новый SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Установите переменные
heroku config:set SECRET_KEY="ваш-новый-секретный-ключ"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
heroku config:set CORS_ALLOW_ALL_ORIGINS=False
heroku config:set CORS_ALLOWED_ORIGINS="https://ваш-фронтенд-домен.com"
```

### 6. Инициализируйте Git и деплойте
```bash
git init
git add .
git commit -m "Initial commit for Heroku"
git push heroku main
```

### 7. Запустите миграции
```bash
heroku run python manage.py migrate
```

### 8. Создайте суперпользователя (опционально)
```bash
heroku run python manage.py createsuperuser
```

### 9. Соберите статические файлы
```bash
heroku run python manage.py collectstatic --noinput
```

### 10. Откройте приложение
```bash
heroku open
```

## Проверка логов
```bash
heroku logs --tail
```

## Полезные команды

### Перезапустить приложение
```bash
heroku restart
```

### Открыть консоль Django
```bash
heroku run python manage.py shell
```

### Посмотреть переменные окружения
```bash
heroku config
```

### Загрузить файлы на Heroku
Для медиа-файлов рекомендуется использовать внешнее хранилище (AWS S3, Cloudinary и т.д.)

## Важные замечания:

1. **SECRET_KEY** - обязательно создайте новый для production!
2. **ALLOWED_HOSTS** - добавьте ваш домен Heroku
3. **CORS_ALLOWED_ORIGINS** - добавьте URL вашего фронтенда
4. **Медиа-файлы** - Heroku имеет эфемерную файловую систему, используйте AWS S3 или Cloudinary
5. **База данных** - используйте Heroku PostgreSQL, не SQLite

## Для локальной разработки:

Создайте файл `.env` в папке backend (скопируйте из `.env.example`):
```bash
SECRET_KEY=django-insecure-x@+#o6)za8rtb7lv!cd+y5+f*k11&jl*pqd$7dum%nkxx%pq2z
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```
