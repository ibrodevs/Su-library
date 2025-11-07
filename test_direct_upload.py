#!/usr/bin/env python
"""
Тест прямой загрузки файла в Spaces
"""
import os
import django
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.files.base import ContentFile
from backend.storage_backends import MediaStorage

print("=" * 60)
print("ТЕСТ ПРЯМОЙ ЗАГРУЗКИ В SPACES")
print("=" * 60)

try:
    # Создаем экземпляр хранилища
    storage = MediaStorage()
    
    print(f"Storage location: {storage.location}")
    print(f"Storage bucket: {storage.bucket_name}")
    print()
    
    # Создаем тестовый файл
    test_content = b"Test file content for upload verification"
    test_file = ContentFile(test_content)
    
    # Пытаемся сохранить
    print("Загрузка тестового файла...")
    filename = "test/direct_upload_test.txt"
    
    saved_name = storage.save(filename, test_file)
    print(f"✅ Файл сохранен: {saved_name}")
    
    # Получаем URL
    url = storage.url(saved_name)
    print(f"✅ URL: {url}")
    
    # Проверяем существование
    exists = storage.exists(saved_name)
    print(f"Файл существует (exists): {exists}")
    
    # Удаляем тестовый файл
    storage.delete(saved_name)
    print(f"✅ Тестовый файл удален")
    
    print()
    print("=" * 60)
    print("✅ ВСЕ РАБОТАЕТ! Spaces подключен правильно.")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()
