# core/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import PhoneNumberOTP

User = get_user_model()

class PhoneOTPBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, otp_code=None):
        if not (phone_number and otp_code):
            return None

        try:
            otp_entry = PhoneNumberOTP.objects.get(phone_number=phone_number, otp_code=otp_code)
        except PhoneNumberOTP.DoesNotExist:
            return None

        if otp_entry.is_valid():
            otp_entry.is_verified = True # Помечаем OTP как использованный
            otp_entry.save()

            user, created = User.objects.get_or_create(phone_number=phone_number)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None