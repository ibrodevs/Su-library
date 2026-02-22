from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Бэкенд аутентификации, позволяющий логиниться через email или username.
    Необходим, так как модель User использует email в качестве USERNAME_FIELD.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Пытаемся найти пользователя по email или username
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Если по email не найден, ищем по username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        # Проверяем пароль
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
