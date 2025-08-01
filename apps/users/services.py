import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

def send_otp(phone_number: str, otp_code: str):
    """
    Отправляет OTP-код на указанный номер телефона.
    """
    response = requests.get(f"https://gateway.api.sc/telegram-code/?login=79131887263&pass=;8zJK%1zwk&code={otp_code}&phone={phone_number.strip('+')}")
    return response.status_code == 200


def is_user_ban(request, phone_number: str, ):
    """ Проверяет забанен ли пользователь """
    if User.objects.filter(phone_number=phone_number).exists():
        if not User.objects.get(phone_number=phone_number).is_active:
            messages.error(request, message='Вы были заблокированы за многократные нарушения')
            return True
