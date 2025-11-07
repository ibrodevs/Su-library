import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
from main.models import Book

print("=" * 50)
print("STORAGE CONFIGURATION CHECK")
print("=" * 50)

print(f"\n1. USE_SPACES: {settings.USE_SPACES}")
print(f"2. DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"3. MEDIA_URL: {settings.MEDIA_URL}")

# Проверяем что используют поля модели
book = Book()
print(f"\n4. Book.pdf_file.storage type: {type(book.pdf_file.storage).__name__}")
print(f"5. Book.pdf_file.storage class: {book.pdf_file.storage.__class__.__module__}.{book.pdf_file.storage.__class__.__name__}")
print(f"6. Book.cover_image.storage type: {type(book.cover_image.storage).__name__}")
print(f"7. Book.cover_image.storage class: {book.cover_image.storage.__class__.__module__}.{book.cover_image.storage.__class__.__name__}")

# Проверяем настройки storage
if hasattr(book.pdf_file.storage, 'location'):
    print(f"\n8. Storage location: '{book.pdf_file.storage.location}'")
if hasattr(book.pdf_file.storage, 'bucket_name'):
    print(f"9. Storage bucket: {book.pdf_file.storage.bucket_name}")
if hasattr(book.pdf_file.storage, 'endpoint_url'):
    print(f"10. Storage endpoint: {book.pdf_file.storage.endpoint_url}")

print("\n" + "=" * 50)
