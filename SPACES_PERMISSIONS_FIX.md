# Исправление ошибки 403 в DigitalOcean Spaces

## Проблема
При загрузке файлов через админку Django возникает ошибка:
```
An error occurred (403) when calling the HeadObject operation: Forbidden
```

## Причина
DigitalOcean Spaces не дает права на выполнение операции `head_object` с текущими ключами доступа.

## Решения

### Решение 1: Настройка прав Space (Рекомендуется)

1. Зайдите в DigitalOcean Dashboard
2. Перейдите в **Spaces** → **su-library**
3. Во вкладке **Settings**:
   - Убедитесь, что Space имеет **Public** доступ на чтение
   - Или установите **Private** и настройте CORS правильно

### Решение 2: Регенерация ключей доступа

1. В DigitalOcean перейдите в **API** → **Spaces access keys**
2. Удалите старые ключи
3. Создайте новые ключи с полными правами (Read & Write)
4. Обновите переменные окружения на Heroku:
```bash
heroku config:set AWS_ACCESS_KEY_ID=новый_ключ --app su-library-back
heroku config:set AWS_SECRET_ACCESS_KEY=новый_секрет --app su-library-back
```

### Решение 3: Настройка Space ACL

1. В Space **su-library** проверьте File Listing:
   - Если установлен как Private, измените на Public для чтения
2. Или настройте Bucket Policy для вашего приложения

### Решение 4: CORS настройки (если используете CDN)

Если вы планируете использовать CDN, добавьте CORS правила в Space:

1. В Space → **Settings** → **CORS Configurations**
2. Добавьте правило:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>*</AllowedHeader>
  </CORSRule>
</CORSConfiguration>
```

## Временное решение в коде

Мы уже добавили обход проблемы в `backend/storage_backends.py`:
- Метод `exists()` переопределен и всегда возвращает `False`
- Это отключает проверку существования файла через `head_object`
- Файлы будут загружаться напрямую без проверки

**Внимание**: Это временное решение. Правильнее всего настроить права доступа в Space.

## Проверка после исправления

После применения любого из решений:

1. Попробуйте загрузить файл через админку
2. Проверьте, что файл появился в Space
3. Проверьте, что файл доступен по URL

## Текущие настройки

Space: `su-library`
Region: `blr1`
Endpoint: `https://blr1.digitaloceanspaces.com`
Custom Domain: `su-library.blr1.digitaloceanspaces.com`
