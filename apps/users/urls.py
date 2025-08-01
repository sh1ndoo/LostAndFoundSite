from django.contrib import admin
from django.urls import include, path

from apps.users.views import RequestOTPView, VerifyOTPView, UserProfileView, UserProfileUpdateView, UserLogoutView, \
    resend_otp

app_name = "users"
urlpatterns = [
    path('login/', RequestOTPView.as_view(), name='login'),  # URL для входа
    path('resend-otp/', resend_otp, name='resend_otp'),  # URL для повторной отправки OTP
    path('logout/', UserLogoutView.as_view(), name='logout'), # URL для выхода
    path('verify/', VerifyOTPView.as_view(), name='verify_otp'),  # URL для верификации OTP
    path('profile/<int:id>', UserProfileView.as_view(), name='profile'),  # URL для профиля пользователя
    path('edit/', UserProfileUpdateView.as_view(), name='edit_profile'),  # URL для редактирования профиля пользователя
]
