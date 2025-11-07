"""
Скрипт для установки public-read ACL на конкретный файл
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
import boto3

print("=" * 60)
print("FIXING SPECIFIC FILE ACL")
print("=" * 60)

# Создаем S3 клиент
s3_client = boto3.client(
    's3',
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

bucket = settings.AWS_STORAGE_BUCKET_NAME
file_key = 'media/books/covers/2025/11/07/1686099911_polinka-top-p-zanyatiya-sportom-kartinki-dlya-prezentats-31.png'

print(f"\nБакет: {bucket}")
print(f"Файл: {file_key}")

try:
    # Проверяем, существует ли файл
    print("\n1. Проверка существования файла...")
    response = s3_client.head_object(Bucket=bucket, Key=file_key)
    print(f"   ✅ Файл существует, размер: {response['ContentLength']} bytes")
    
    # Устанавливаем public-read ACL
    print("\n2. Установка public-read ACL...")
    s3_client.put_object_acl(
        Bucket=bucket,
        Key=file_key,
        ACL='public-read'
    )
    print("   ✅ ACL установлен на public-read")
    
    # Проверяем URL
    url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_key}"
    print(f"\n3. URL файла:")
    print(f"   {url}")
    print(f"\n✅ Попробуйте открыть URL в браузере!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n" + "=" * 60)
