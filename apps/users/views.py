# core/views.py
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView, UpdateView

from .forms import PhoneNumberForm, OTPForm, EditProfileForm
from .models import PhoneNumberOTP

from .services import *

User = get_user_model()

def send_otp_complete(request, phone_number):
    """Отправка OTP кода с проверками на валидность"""
    if not phone_number:
        messages.error(request, "Номер телефона не найден в сессии.")
        return redirect('users:login')

    if is_user_ban(request, phone_number):
        return redirect('users:login')

    otp_entry, created = PhoneNumberOTP.objects.get_or_create(phone_number=phone_number)

    if not otp_entry.is_old():
        messages.error(request,
                       message=f'Код подтверждения уже был отправлен. Пожалуйста, подождите {otp_entry.time_to_old().seconds} секунд перед повторной отправкой.')
        return redirect('users:verify_otp')

    otp_code = otp_entry.generate_otp()

    if send_otp(phone_number, otp_code):
        request.session['phone_for_otp'] = phone_number
        return redirect('users:verify_otp')
    else:
        messages.error(request, "Не удалось отправить код подтверждения. Используйте другой способ входа")
        return redirect('users:login')

class RequestOTPView(View):
    template_name = 'users/enter_phone.html'

    def get(self, request):
        form = PhoneNumberForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            send_otp_complete(request, phone_number)
        return render(request, self.template_name, {'form': form})


class VerifyOTPView(View):
    template_name = 'users/verify_otp.html'

    def get(self, request):
        phone_number = request.session.get('phone_for_otp')
        if not phone_number:
            return redirect('request_otp')
        return render(request, self.template_name, {'phone_number': phone_number})

    def post(self, request):
        phone_number = request.session.get('phone_for_otp')

        otp_code = request.POST.get('otp_code')
        user = authenticate(request, phone_number=phone_number, otp_code=otp_code)

        if user:
            login(request, user)
            del request.session['phone_for_otp']
            return redirect('/')
        else:
            messages.error(request, "Неверный код подтверждения или он истек. Пожалуйста, попробуйте еще раз.")
        return render(request, self.template_name, {'phone_number': phone_number})

class UserLogoutView(LogoutView):
    pass

class UserProfileView(DetailView):
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user'
    slug_field = 'id'
    slug_url_kwarg = 'id'

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_update.html'
    form_class = EditProfileForm

    def get_object(self):
        return self.request.user

@require_GET
def resend_otp(request):
    phone_number = request.session.get('phone_for_otp')
    send_otp_complete(request, phone_number)

