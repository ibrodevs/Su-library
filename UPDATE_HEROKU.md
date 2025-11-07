# Обновление настроек на Heroku

## Домены проекта:
- **Backend:** https://su-library-back-d2d8d21af2e4.herokuapp.com
- **Frontend:** http://su-library.com и https://su-e-library.vercel.app

## Команды для обновления на Heroku:

### 1. Установите переменные окружения на Heroku:

```bash
cd backend

# Установите ALLOWED_HOSTS
heroku config:set ALLOWED_HOSTS="localhost,127.0.0.1,su-library-back-d2d8d21af2e4.herokuapp.com"

# Установите CORS_ALLOWED_ORIGINS (важно для работы с фронтендом)
heroku config:set CORS_ALLOWED_ORIGINS="http://su-library.com,https://su-library.com,https://su-e-library.vercel.app"

# Установите CORS_ALLOW_ALL_ORIGINS в False для безопасности
heroku config:set CORS_ALLOW_ALL_ORIGINS=False

# Проверьте, что DEBUG=False
heroku config:set DEBUG=False

# Если ещё не установили SECRET_KEY, создайте новый:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
heroku config:set SECRET_KEY="сгенерированный-ключ"
```

### 2. Задеплойте обновленный код:

```bash
# Убедитесь, что вы в папке backend
cd backend

# Добавьте изменения в git
git add .
git commit -m "Update settings for production domains"

# Задеплойте на Heroku
git push heroku main
```

### 3. Проверьте настройки:

```bash
# Посмотрите все переменные окружения
heroku config

# Проверьте логи
heroku logs --tail
```

### 4. Перезапустите приложение (если нужно):

```bash
heroku restart
```

## Проверка работы CORS:

После деплоя проверьте, что фронтенд может обращаться к API:
- Откройте http://su-library.com в браузере
- Откройте Developer Tools (F12) → Console
- Не должно быть ошибок CORS

## Если используете кастомный домен для backend:

Если хотите использовать свой домен вместо herokuapp.com:

```bash
# Добавьте домен на Heroku
heroku domains:add api.su-library.com

# Обновите DNS записи у вашего регистратора домена
# Добавьте CNAME запись: api.su-library.com → su-library-back-d2d8d21af2e4.herokuapp.com

# Обновите настройки:
heroku config:set ALLOWED_HOSTS="localhost,127.0.0.1,su-library-back-d2d8d21af2e4.herokuapp.com,api.su-library.com"
```

## Важно:

1. **SECRET_KEY** должен быть уникальным для production
2. **DEBUG=False** обязательно для production
3. **CORS_ALLOW_ALL_ORIGINS=False** для безопасности (разрешаем только конкретные домены)
4. Все домены фронтенда должны быть в CORS_ALLOWED_ORIGINS
