from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-3",
                "placeholder": "Имя пользователя",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control py-3",
                "placeholder": "Пароль",
            }
        )
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control py-3", "placeholder": "Email"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control py-3", "placeholder": "Имя пользователя"}
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-3", "placeholder": "Пароль"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-3", "placeholder": "Повторите пароль"}
        )
    )
