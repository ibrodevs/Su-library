#!/usr/bin/env python
"""
Список всех файлов в DigitalOcean Spaces
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
import boto3

# Создаем клиент S3
s3_client = boto3.client(
    's3',
    region_name=settings.AWS_S3_REGION_NAME,
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

print("=" * 60)
print("СПИСОК ФАЙЛОВ В DIGITALOCEAN SPACES")
print("=" * 60)
print(f"Bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
print(f"Endpoint: {settings.AWS_S3_ENDPOINT_URL}")
print()

try:
    # Получаем список ВСЕХ объектов (включая в папках)
    response = s3_client.list_objects_v2(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        MaxKeys=1000
    )
    
    print(f"HTTP Status: {response['ResponseMetadata']['HTTPStatusCode']}")
    print(f"Bucket exists and accessible: ✅\n")
    
    if 'Contents' in response:
        print(f"Найдено файлов: {len(response['Contents'])}\n")
        
        for obj in response['Contents']:
            size_kb = obj['Size'] / 1024
            print(f"📄 {obj['Key']}")
            print(f"   Размер: {size_kb:.2f} KB")
            print(f"   Дата: {obj['LastModified']}")
            print()
    else:
        print("❌ Space пустой - файлов не найдено")
        print("\nВозможные причины:")
        print("1. Файлы не загружаются из-за ошибки")
        print("2. Права доступа к Bucket ограничены")
        print("3. Bucket действительно пустой")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print(f"Тип ошибки: {type(e).__name__}")

print("=" * 60)
