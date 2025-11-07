# Быстрая настройка DigitalOcean Spaces

## Что это дает?

✅ **CDN** - быстрая доставка файлов по всему миру  
✅ **Масштабируемость** - неограниченное хранилище  
✅ **Производительность** - разгрузка сервера от раздачи статики  
✅ **Надежность** - репликация и высокая доступность  

## Быстрый старт (3 шага) ✅ УЖЕ НАСТРОЕНО

### ✅ 1. Space создан

- **Имя**: `su-library`
- **Регион**: Bangalore (blr1)
- **CDN**: Включен
- **URL**: https://su-library.blr1.digitaloceanspaces.com

### ✅ 2. Ключи доступа получены

- **Key Name**: key-1762493805669
- **Access Key**: DO801328JW7UKUFKDWJJ
- **Secret Key**: ✅ Сохранен

### 3. Настройте CORS (если еще не сделано)

В вашем Space → **Settings** → **CORS Configurations**:

```
Origin: https://su-e-library.vercel.app
Methods: GET, PUT, POST, DELETE, HEAD
Headers: *
```

### 4. Добавьте переменные окружения

В DigitalOcean App Platform → ваше приложение → **Settings** → **Environment Variables**:

```env
USE_SPACES=True
AWS_ACCESS_KEY_ID=DO801328JW7UKUFKDWJJ
AWS_SECRET_ACCESS_KEY=MeSNvR1wHHPs8CLI1f0aaNhYjxLnQ7YRyS+QeHDDSZs
AWS_STORAGE_BUCKET_NAME=su-library
AWS_S3_ENDPOINT_URL=https://blr1.digitaloceanspaces.com
AWS_S3_REGION_NAME=blr1
AWS_S3_CUSTOM_DOMAIN=su-library.blr1.cdn.digitaloceanspaces.com
```

⚠️ Отметьте ключи как **Encrypted**!

### 5. Пересоберите приложение

В App Platform нажмите **Actions** → **Force Rebuild and Deploy**

## Проверка

После развертывания проверьте:

```bash
# В консоли приложения
python manage.py shell
```

```python
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Тест записи
path = default_storage.save('test.txt', ContentFile(b'Hello!'))
print(f"URL: {default_storage.url(path)}")
# Должно быть: https://su-library.blr1.cdn.digitaloceanspaces.com/media/test.txt
```

## URL файлов

После настройки все загружаемые файлы будут автоматически:
- Сохраняться в DigitalOcean Spaces (`su-library`, регион Bangalore)
- Раздаваться через CDN
- Иметь URL формата: `https://su-library.blr1.cdn.digitaloceanspaces.com/media/books/...`

## Миграция существующих файлов

Если у вас уже есть файлы в `media/`:

### Вариант 1: Веб-интерфейс
Просто перетащите папки в Space через веб-интерфейс

### Вариант 2: s3cmd (автоматически)

```bash
# Установка
pip install s3cmd

# Настройка
s3cmd --configure
# Access Key: ваш ключ
# Secret Key: ваш секретный ключ
# Region: fra1
# S3 Endpoint: fra1.digitaloceanspaces.com

# Загрузка файлов
s3cmd sync ./media/ s3://su-library/media/ --acl-public
```

## Локальная разработка

Для локальной разработки оставьте `USE_SPACES=False` в `.env`:

```env
# .env (локально)
USE_SPACES=False
```

Файлы будут сохраняться локально в `media/`.

## Стоимость

- **$5/месяц** за 250GB хранилища + 1TB трафика
- **$0.01/GB** за дополнительный трафик
- CDN включен бесплатно

## Troubleshooting

### Файлы не загружаются
- ✅ Проверьте ключи доступа
- ✅ Убедитесь что `USE_SPACES=True`
- ✅ Проверьте CORS настройки

### 403 или Access Denied
- ✅ Проверьте права доступа к Space
- ✅ `AWS_DEFAULT_ACL = 'public-read'` в settings.py

### Файлы не отображаются на фронте
- ✅ Проверьте CORS
- ✅ Правильный CDN домен в `AWS_S3_CUSTOM_DOMAIN`

## Полная документация

См. [DIGITALOCEAN_DEPLOY.md](./DIGITALOCEAN_DEPLOY.md) для подробных инструкций.
