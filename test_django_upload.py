#!/usr/bin/env python
"""
Тест загрузки файла через Django модель
"""
import os
import django
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.files.base import ContentFile
from main.models import Book, Category
from django.conf import settings

print("=" * 60)
print("ТЕСТ ЗАГРУЗКИ ФАЙЛА ЧЕРЕЗ DJANGO")
print("=" * 60)
print(f"USE_SPACES: {settings.USE_SPACES}")
print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print()

try:
    # Создаем категорию если нет
    category, created = Category.objects.get_or_create(
        defaults={'is_active': True}
    )
    print(f"✅ Категория: {category.id}")
    
    # Создаем тестовую книгу
    book = Book()
    book.category = category
    book.year = 2025
    book.is_active = True
    
    # Создаем тестовый PDF файл
    pdf_content = b"%PDF-1.4 Test PDF content"
    pdf_file = ContentFile(pdf_content, name='test_book.pdf')
    
    # Создаем тестовое изображение (простой PNG)
    image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    image_file = ContentFile(image_content, name='test_cover.png')
    
    # Присваиваем файлы
    book.pdf_file = pdf_file
    book.cover_image = image_file
    
    print("Попытка сохранить книгу...")
    book.save()
    
    print(f"✅ Книга создана: ID={book.id}")
    print(f"   PDF: {book.pdf_file.name}")
    print(f"   PDF URL: {book.pdf_file.url}")
    print(f"   Обложка: {book.cover_image.name}")
    print(f"   Обложка URL: {book.cover_image.url}")
    
    # Проверяем, что файл существует
    print("\nПроверка существования файлов:")
    pdf_storage = book.pdf_file.storage
    cover_storage = book.cover_image.storage
    
    print(f"   PDF exists: {pdf_storage.exists(book.pdf_file.name)}")
    print(f"   Cover exists: {cover_storage.exists(book.cover_image.name)}")
    
    print("\n✅ ТЕСТ УСПЕШЕН!")
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    print(f"Тип: {type(e).__name__}")
    import traceback
    print("\nТрейсбек:")
    traceback.print_exc()

print("=" * 60)
