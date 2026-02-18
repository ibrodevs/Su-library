# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, ProfileSerializer, ChangePasswordSerializer


# --- Вход (логин) ---
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  # этот эндпоинт открытый, без токена

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        # Создаём токены для пользователя
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


# --- Профиль (только для авторизованных) ---
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # request.user — это текущий авторизованный пользователь
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


# --- Смена пароля ---
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Проверяем старый пароль
        if not user.check_password(old_password):
            return Response(
                {'error': 'Неверный старый пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Пароль успешно изменён.'})