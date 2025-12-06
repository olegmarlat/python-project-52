from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth')


class CustomUserUpdateForm(UserChangeForm):
    password = None  # Убираем поле пароля из формы редактирования

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'is_active')