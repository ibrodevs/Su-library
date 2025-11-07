#!/usr/bin/env python
"""Upload test file to Spaces"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from backend.storage_backends import MediaStorage

storage = MediaStorage()

# Пробуем загрузить тестовый файл
test_content = b"Hello from Django!"
test_filename = "media/test_upload.txt"

try:
    # Сохраняем файл
    saved_path = storage.save(test_filename, ContentFile(test_content))
    print(f"✅ Файл успешно загружен!")
    print(f"Путь: {saved_path}")
    print(f"URL: {storage.url(saved_path)}")
    
    # Проверяем, можем ли прочитать
    try:
        with storage.open(saved_path, 'rb') as f:
            content = f.read()
            print(f"✅ Файл прочитан: {content.decode()}")
    except Exception as e:
        print(f"❌ Ошибка чтения: {e}")
    
    # Пробуем удалить
    try:
        storage.delete(saved_path)
        print(f"✅ Файл удален")
    except Exception as e:
        print(f"⚠️  Ошибка удаления: {e}")
        
except Exception as e:
    print(f"❌ Ошибка загрузки: {e}")
    import traceback
    traceback.print_exc()
