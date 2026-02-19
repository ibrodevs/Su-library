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
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'group', 'course', 'is_active', 'is_staff', 'password',]
        # Если в модели есть group и course — добавь их:
        # fields = ['first_name', 'last_name', 'email', 'group', 'course']
        read_only_fields = ['is_active', 'is_staff']

# --- Сериализатор для смены пароля ---
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверный")
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Новый пароль должен быть минимум 6 символов")
        return value