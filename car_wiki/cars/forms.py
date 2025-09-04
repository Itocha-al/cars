from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Адрес электронной почты",
        help_text="Обязательно для заполнения",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="Имя пользователя",
        help_text="Не более 150 символов. Только буквы, цифры и @/./+/-/_",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Пароль",
        help_text="""
            <ul>
                <li>Пароль не должен быть слишком похож на другую вашу личную информацию</li>
                <li>Пароль должен содержать как минимум 8 символов</li>
                <li>Пароль не может быть одним из часто используемых паролей</li>
                <li>Пароль не может состоять только из цифр</li>
            </ul>
        """,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        help_text="Введите тот же пароль, для подтверждения",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Имя пользователя'),
            'email': _('Электронная почта'),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
