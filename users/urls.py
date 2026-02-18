# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # встроенный view для refresh

from .views import LoginView, ProfileView, ChangePasswordView

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/change-password/', ChangePasswordView.as_view()),
]