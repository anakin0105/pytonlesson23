# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя"""

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'country', 'avatar', 'password1', 'password2']
        labels = {
            'email': 'Email адрес',
            'username': 'Имя пользователя',
            'phone_number': 'Номер телефона',
            'country': 'Страна',
            'avatar': 'Аватар',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'country', 'avatar']
        labels = {
            'email': 'Email адрес',
            'username': 'Имя пользователя',
            'phone_number': 'Номер телефона',
            'country': 'Страна',
            'avatar': 'Аватар',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})