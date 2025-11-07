"""
Кастомные storage классы для DigitalOcean Spaces
"""
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Хранилище для статических файлов (CSS, JS, изображения приложения)"""
    location = 'static'
    default_acl = None  # Используем настройки Space по умолчанию
    file_overwrite = True


class MediaStorage(S3Boto3Storage):
    """Хранилище для медиа файлов (загружаемые пользователями файлы)"""
    location = 'media'  # Все файлы будут в папке media/
    default_acl = None  # Используем настройки Space по умолчанию
    file_overwrite = False  # Не перезаписывать файлы с одинаковыми именами
    
    # Отключаем gzip для медиа файлов (PDF, изображения)
    gzip = False
    
    def exists(self, name):
        """
        Переопределяем метод exists, чтобы избежать head_object запроса,
        который вызывает 403 Forbidden из-за прав доступа к Space
        """
        return False  # Всегда возвращаем False, чтобы файл загружался
