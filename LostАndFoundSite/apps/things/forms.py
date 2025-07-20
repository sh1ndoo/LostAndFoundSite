from django import forms

from apps.things.models import Thing


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        exclude = ('owner',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'style': 'display: none;',
                'accept': 'image/*',
                'id': 'image'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адреcc, где была потеряна или найдена вещь'
            }),
            'date_lost_or_found': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Примерная дата пропажи/находки'
            }),
        }
