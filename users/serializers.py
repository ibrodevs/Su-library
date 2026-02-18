# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()  # берём модель пользователя из проекта


# --- Сериализатор для логина ---
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # write_only = не возвращаем пароль в ответе

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Проверяем что поля не пустые
        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны.")

        # Пытаемся найти пользователя
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Неверный email или пароль.")

        data['user'] = user
        return data


# --- Сериализатор для профиля ---
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # Если в модели есть group и course — добавь их:
        # fields = ['first_name', 'last_name', 'email', 'group', 'course']


# --- Сериализатор для смены пароля ---
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)