from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        strip=False,
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
            "username": _("Имя пользователя"),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _("Пароли не совпадают."),
                code="password_mismatch",
            )
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) < 3:
            raise ValidationError(
                _(
                    "Этот пароль слишком короткий. "
                    "Он должен содержать не менее 3 символов."
                ),
                code="password_too_short",
            )
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput,
        strip=False,
        required=False,
    )
    password2 = forms.CharField(
        label=_("Подтверждение нового пароля"),
        widget=forms.PasswordInput,
        strip=False,
        required=False,
    )
    username = forms.CharField(
        label=_("Имя пользователя"),
        disabled=True,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if not password1 or not password2:
                self.add_error(
                    "password2",
                    _("Пожалуйста, заполните оба поля для пароля.")
                )
            elif password1 != password2:
                self.add_error("password2", _("Пароли не совпадают."))
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) < 3:
            raise ValidationError(
                _(
                    "Этот пароль слишком короткий. "
                    "Он должен содержать не менее 3 символов."
                ),
                code="password_too_short",
            )
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
