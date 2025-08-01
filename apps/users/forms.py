from django import forms
from django.contrib.auth import get_user_model


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        label="Номер телефона",
        max_length=25,
        widget=forms.TextInput(attrs={"type": "tel", "id": "phone", "name": "phone",
                           "placeholder": "+7 (XXX) XXX-XX-XX",
                           "pattern": r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$",
                           "title": "Введите номер телефона в формате +7 (XXX) XXX-XX-XX",
                           "inputmode": "numeric"})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = phone_number.replace(' ', '').replace('-', '').replace(')', '').replace('(', '').replace(')', '')
        if not phone_number.startswith('+'):
            raise forms.ValidationError("Номер телефона должен начинаться с '+'.")
        return phone_number

class OTPForm(forms.Form):
    otp_code = forms.CharField(
        label="Код подтверждения",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'XXXXXX'})
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model() 
        fields = ('first_name', 'telegram', 'vk', 'avatar')