"""
Кастомные storage классы для DigitalOcean Spaces
"""
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)


class StaticStorage(S3Boto3Storage):
    """Хранилище для статических файлов (CSS, JS, изображения приложения)"""
    location = 'static'
    default_acl = None  # Используем настройки Space по умолчанию
    file_overwrite = True


class MediaStorage(S3Boto3Storage):
    """Хранилище для медиа файлов (загружаемые пользователями файлы)"""
    location = 'media'  # Сохраняем файлы в папку media/ в Spaces
    default_acl = None  # Используем настройки Space по умолчанию
    file_overwrite = False  # Не перезаписывать файлы с одинаковыми именами
    
    # Отключаем gzip для медиа файлов (PDF, изображения)
    gzip = False
    
    def exists(self, name):
        """
        Переопределяем метод exists, чтобы избежать head_object запроса,
        который вызывает 403 Forbidden из-за прав доступа к Space
        """
        logger.info(f"MediaStorage.exists() called for: {name}")
        return False  # Всегда возвращаем False, чтобы файл загружался
    
    def save(self, name, content, max_length=None):
        """Добавляем логирование для отладки"""
        logger.info(f"MediaStorage.save() called - name: {name}, content type: {type(content)}, size: {getattr(content, 'size', 'unknown')}")
        try:
            result = super().save(name, content, max_length)
            logger.info(f"MediaStorage.save() SUCCESS - saved as: {result}")
            return result
        except Exception as e:
            logger.error(f"MediaStorage.save() FAILED - error: {e}", exc_info=True)
            raise
