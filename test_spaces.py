#!/usr/bin/env python
"""
Скрипт для проверки подключения к DigitalOcean Spaces
Использование: python test_spaces.py
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def test_spaces_connection():
    """Тестирование подключения к DigitalOcean Spaces"""
    
    print("=" * 60)
    print("ПРОВЕРКА ПОДКЛЮЧЕНИЯ К DIGITALOCEAN SPACES")
    print("=" * 60)
    print()
    
    # Проверка настроек
    print("1. Проверка настроек:")
    print(f"   USE_SPACES: {getattr(settings, 'USE_SPACES', False)}")
    
    if not getattr(settings, 'USE_SPACES', False):
        print("\n❌ USE_SPACES=False - используются локальные файлы")
        print("   Установите USE_SPACES=True для использования Spaces")
        return False
    
    print(f"   Bucket: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'не задан')}")
    print(f"   Region: {getattr(settings, 'AWS_S3_REGION_NAME', 'не задан')}")
    print(f"   Endpoint: {getattr(settings, 'AWS_S3_ENDPOINT_URL', 'не задан')}")
    print(f"   CDN Domain: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'не задан')}")
    print()
    
    # Проверка ключей
    print("2. Проверка ключей доступа:")
    access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    
    if access_key:
        print(f"   ✅ Access Key: {access_key[:8]}...{access_key[-4:]}")
    else:
        print("   ❌ Access Key не найден")
        return False
        
    if secret_key:
        print(f"   ✅ Secret Key: {'*' * 20}")
    else:
        print("   ❌ Secret Key не найден")
        return False
    print()
    
    # Тест записи
    print("3. Тест записи файла:")
    test_content = b'Test file created at ' + str(os.times()).encode()
    test_filename = 'test/connection_test.txt'
    
    try:
        path = default_storage.save(test_filename, ContentFile(test_content))
        print(f"   ✅ Файл создан: {path}")
    except Exception as e:
        print(f"   ❌ Ошибка при создании: {e}")
        return False
    print()
    
    # Тест чтения URL
    print("4. Тест получения URL:")
    try:
        url = default_storage.url(path)
        print(f"   ✅ URL: {url}")
        
        if 'digitaloceanspaces.com' in url:
            print("   ✅ URL содержит digitaloceanspaces.com")
        else:
            print("   ⚠️  URL не содержит digitaloceanspaces.com")
            
        if '.cdn.' in url:
            print("   ✅ Используется CDN")
        else:
            print("   ⚠️  CDN не используется")
    except Exception as e:
        print(f"   ❌ Ошибка при получении URL: {e}")
        return False
    print()
    
    # Тест чтения
    print("5. Тест чтения файла:")
    try:
        file = default_storage.open(path)
        content = file.read()
        file.close()
        print(f"   ✅ Файл прочитан: {len(content)} байт")
    except Exception as e:
        print(f"   ❌ Ошибка при чтении: {e}")
        return False
    print()
    
    # Тест проверки существования
    print("6. Тест проверки существования:")
    try:
        exists = default_storage.exists(path)
        print(f"   ✅ Файл существует: {exists}")
    except Exception as e:
        print(f"   ❌ Ошибка при проверке: {e}")
        return False
    print()
    
    # Тест удаления
    print("7. Тест удаления файла:")
    try:
        default_storage.delete(path)
        print(f"   ✅ Файл удален")
        
        # Проверка что удален
        exists = default_storage.exists(path)
        if not exists:
            print(f"   ✅ Подтверждено: файл не существует")
        else:
            print(f"   ⚠️  Файл все еще существует")
    except Exception as e:
        print(f"   ❌ Ошибка при удалении: {e}")
        return False
    print()
    
    print("=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 60)
    print()
    print("DigitalOcean Spaces настроен правильно и готов к использованию.")
    print()
    
    return True

def show_current_storage_info():
    """Показать информацию о текущем хранилище"""
    print("\nИнформация о текущем хранилище:")
    print(f"  Backend: {default_storage.__class__.__name__}")
    print(f"  Module: {default_storage.__class__.__module__}")
    
    if hasattr(default_storage, 'bucket_name'):
        print(f"  Bucket: {default_storage.bucket_name}")
    if hasattr(default_storage, 'endpoint_url'):
        print(f"  Endpoint: {default_storage.endpoint_url}")
    print()

if __name__ == '__main__':
    try:
        show_current_storage_info()
        success = test_spaces_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nТест прерван пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
