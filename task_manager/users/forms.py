from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from django.contrib.auth.forms import AuthenticationForm


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class BaseUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
        help_texts = {
            "username": _(
                "Required. 150 characters or fewer. "
                "Letters, digits and @/./+/-/_ only."
            ),
        }


class CustomUserCreationForm(FormStyleMixin, UserCreationForm):
    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, "password1", "password2")
        help_texts = {
            **BaseUserForm.Meta.help_texts,
            "password1": _("Your password must contain at least 3 characters."),
            "password2": _("Please enter your password again to confirm."),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", _("Passwords don't match."))
            elif len(password1) < 3:
                self.add_error(
                    "password2",
                    _(
                        "This password is too short. It must contain at least 3 characters."
                    ),
                )
        return cleaned_data


class CustomUserChangeForm(FormStyleMixin, forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Leave blank to keep current password."),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Enter new password again to confirm."),
    )

    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if not password1 or not password2:
                self.add_error("password2", _("Please fill both password fields."))
            elif password1 != password2:
                self.add_error("password2", _("Passwords don't match."))
            elif len(password1) < 3:
                self.add_error(
                    "password2",
                    _(
                        "This password is too short. It must contain at least 3 characters."
                    ),
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if password1 := self.cleaned_data.get("password1"):
            user.set_password(password1)
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(FormStyleMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем placeholder'ы
        self.fields["username"].widget.attrs.update(
            {"placeholder": _("Имя пользователя")}
        )
        self.fields["password"].widget.attrs.update(
            {"placeholder": _("Пароль")}
        )
