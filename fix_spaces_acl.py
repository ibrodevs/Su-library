"""
Скрипт для установки public-read ACL на все файлы в DigitalOcean Spaces
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
import boto3

print("=" * 60)
print("FIXING SPACES FILES ACL")
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

print(f"\nБакет: {bucket}")
print(f"Endpoint: {settings.AWS_S3_ENDPOINT_URL}")
print("\nПоиск файлов в папке media/...")

try:
    # Получаем список всех файлов в папке media/
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix='media/'
    )
    
    if 'Contents' not in response:
        print("❌ Файлы не найдены в папке media/")
    else:
        files = response['Contents']
        print(f"\n✅ Найдено файлов: {len(files)}\n")
        
        for obj in files:
            key = obj['Key']
            print(f"Обработка: {key}")
            
            try:
                # Устанавливаем public-read ACL
                s3_client.put_object_acl(
                    Bucket=bucket,
                    Key=key,
                    ACL='public-read'
                )
                print(f"  ✅ ACL установлен на public-read")
                
                # Проверяем URL
                url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}"
                print(f"  📎 URL: {url}\n")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}\n")
        
        print("=" * 60)
        print("ГОТОВО!")
        print("=" * 60)
        
except Exception as e:
    print(f"❌ Ошибка при получении списка файлов: {e}")
