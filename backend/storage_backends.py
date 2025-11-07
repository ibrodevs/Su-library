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
    
    # Важно: отключаем проверку существования перед загрузкой
    # Это решает проблему с 403 Forbidden при head_object
    def get_available_name(self, name, max_length=None):
        """
        Переопределяем метод, чтобы не проверять существование файла
        перед загрузкой (избегаем head_object запрос)
        """
        if self.file_overwrite:
            return name
        return super(S3Boto3Storage, self).get_available_name(name, max_length)
