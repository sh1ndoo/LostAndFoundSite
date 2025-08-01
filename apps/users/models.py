from django.urls import reverse
from django.utils import timezone
import random

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose



class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, email=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        is_superuser = extra_fields.get('is_superuser', False)
        if not is_superuser:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Номер телефона", null=True)

    avatar = ProcessedImageField(verbose_name='Логотип', blank=True, null=True,
                               processors=[
                                            Transpose(),
                                            ResizeToFit(width=300, upscale=False)
                                          ],
                               format='WEBP',
                               options={'quality': 80}, default='base_avatar.webp')
    telegram = models.CharField(max_length=64, blank=True, null=True)
    vk = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True, default='Аноним')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'id': self.pk})

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class PhoneNumberOTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.phone_number}"

    def is_valid(self):
        """Проверяет, действителен ли OTP-код."""
        if not self.expires_at:
            return False
        return timezone.now() < self.expires_at and not self.is_verified

    def time_to_old(self):
        """Возвращает время до возможности повторной генерации OTP."""
        if self.is_valid():
            return self.created_at + timezone.timedelta(minutes=2) - timezone.now()
        return None

    def is_old(self):
        """Проверяет можно ли отправить код повторно"""
        if not self.is_valid():
            return True
        if self.time_to_old() >= timezone.timedelta(minutes=0):
            return False
        return True

    def generate_otp(self):
        """Генерирует новый OTP-код и обновляет время действия."""
        self.otp_code = str(random.randint(100000, 999999))
        self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        self.is_verified = False
        self.save()
        return self.otp_code
