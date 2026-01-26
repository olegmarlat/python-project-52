from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect


from task_manager.mixins import (
    CustomLoginRequiredMixin,
    ProtectErrorMixin,
    UserPermissionMixin,
)
from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)


User = get_user_model()
USERS_INDEX_URL = "users:index"


def index(request):
    return render(request, "users/index.html")


class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["id"]


class BaseUserView(SuccessMessageMixin):
    """Base configuration for user-related views (create/update/delete)."""

    model = User
    template_name = "users/registration_form.html"
    context_object_name = "user"
    permission_denied_url = reverse_lazy(USERS_INDEX_URL)


class UserCreateView(BaseUserView, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    success_message = _("Пользователь успешно зарегистрирован")
    extra_context = {"title": _("Регистрация"),
                     "button_name": _("Зарегистрировать")}


class UserUpdateView(
    CustomLoginRequiredMixin, UserPermissionMixin, BaseUserView, UpdateView
):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy(USERS_INDEX_URL)
    success_message = _("Пользователь успешно изменен")
    permission_denied_message = _("You don't have rights"
                                  "to change another user.")
    extra_context = {
        "title": _("Edit profile"),
        "button_name": _("Изменить"),
    }


class UserDeleteView(
    CustomLoginRequiredMixin,
    UserPermissionMixin,
    ProtectErrorMixin,
    BaseUserView,
    DeleteView,
):
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("users:index")
    success_message = _("Пользователь успешно удален")
    permission_denied_message = _("You don't have rights "
                                  "to change another user.")
    access_denied_message = _("You don't have rights to change another user.")
    protected_object_url = reverse_lazy(USERS_INDEX_URL)
    protected_object_message = _("Cannot delete this user"
                                 "because they are being used")
    extra_context = {
        "title": _("User deletion"),
        "button_name": _("Да, удалить"),
    }


class BaseUserForm:
    """Shared Meta config for user forms."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
        help_texts = {
            "username": _(
                "Required. 150 characters or fewer. "
                "Letters, digits and @/./+/-/_ only."
            ),
        }


class FormStyleMixin:  # noqa: F811
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class CustomUserCreationForm(FormStyleMixin, UserCreationForm):  # noqa: F811
    """User registration form with custom validation and styling."""

    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, "password1", "password2")
        help_texts = {
            **BaseUserForm.Meta.help_texts,
            "password1": _("Your password must contain "
                           "at least 3 characters."),
            "password2": _("Please enter your password again to confirm."),
        }

    def clean(self):
        """Validate password length and equality."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Пропускаем валидацию, если оба поля пустые
        if not password1 and not password2:
            return cleaned_data

        # Проверяем заполненность обоих полей
        if password1 and not password2:
            self.add_error("password2", _("Please confirm your new password."))
        elif password2 and not password1:
            self.add_error("password1", _("Please enter a new password."))

        # Если оба поля заполнены — проверяем совпадение и длину
        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", _("Passwords don't match."))
            elif len(password1) < 3:
                self.add_error(
                    "password2",
                    _("This password is too short."
                      "It must contain at least 3 characters.")
                )

        return cleaned_data


class CustomUserChangeForm(FormStyleMixin, forms.ModelForm):
    """User profile edit form with password update support."""

    password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Your password must contain at least 3 characters."),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Please enter your password again to confirm."),
    )

    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            del self.fields["password"]

    def clean(self):
        """Validate password length and equality."""
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
                        "This password is too short. "
                        "It must contain at least 3 characters."
                    ),
                )
        return cleaned_data

    def save(self, commit=True):
        """Save updated user with new password if provided."""
        user = super().save(commit=False)
        if password1 := self.cleaned_data.get("password1"):
            user.set_password(password1)
        if commit:
            user.save()
        return user


class CustomLoginView(LoginView):
    """Login view with success message and custom form."""

    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response


class CustomLogoutView(BaseLogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Выход из системы
        from django.contrib.auth import logout
        logout(request)
        # сообщение об успешном выходе
        messages.success(request, _("Вы разлогинены"))
        # переход на главную
        return redirect('/')
