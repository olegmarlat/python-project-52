from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.mixins import (
    LoginRequiredMessageMixin,
    ProtectedObjectMixin,
)

User = get_user_model()

USERS_INDEX_URL = "users:index"


class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "users/registration_form.html"
    success_url = reverse_lazy("login")
    success_message = _("Пользователь успешно зарегистрирован")
    extra_context = {
        "title": _("Регистрация"),
        "button_text": _("Зарегистрироваться"),
    }


class UserLoginView(LoginRequiredMessageMixin, SuccessMessageMixin, FormView):
    template_name = "users/login.html"
    success_url = reverse_lazy("index")
    success_message = _("Вы залогинены")
    extra_context = {
        "title": _("Вход"),
        "button_text": _("Войти"),
    }

    def get_form_class(self):
        from django.contrib.auth.forms import AuthenticationForm
        return AuthenticationForm


class UserLogoutView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    success_message = _("Вы разлогинены")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"


class UserUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = User
    template_name = "users/user_form.html"
    success_url = reverse_lazy(USERS_INDEX_URL)
    success_message = _("Пользователь успешно изменен")
    permission_denied_message = _(
        "У вас нет прав для изменения другого пользователя."
    )
    extra_context = {
        "title": _("Редактировать профиль"),
        "button_text": _("Изменить"),
    }

    def get_form_class(self):
        from .forms import UserUpdateForm
        return UserUpdateForm


class UserDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    ProtectedObjectMixin,
    DeleteView
):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:index")
    success_message = _("Пользователь успешно удален")
    permission_denied_message = _(
        "У вас нет прав для изменения другого пользователя."
    )
    access_denied_message = _(
        "У вас нет прав для изменения другого пользователя."
    )
    protected_object_url = reverse_lazy(USERS_INDEX_URL)
    protected_object_message = _(
        "Невозможно удалить пользователя, потому что он используется"
    )
    extra_context = {
        "title": _("Удаление пользователя"),
        "button_text": _("Да, удалить"),
    }
