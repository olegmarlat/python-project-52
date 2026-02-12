from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError


class LoginRequiredMessageMixin:
    login_url = "login"
    permission_denied_message = _("You must be logged in to access this page.")

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You must be logged in to access this page.")
        )
        return redirect(self.login_url)


class ProtectedObjectMixin:
    protected_object_url = None
    protected_object_message = _(
        "Невозможно удалить пользователя, потому что он используется"
    )

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        from task_manager.tasks.models import Task

        # Проверяем обе связи
        if obj.created_tasks.exists() or Task.objects.filter(executor=obj).exists():
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.protected_object_message)
            return redirect(self.protected_object_url)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def handle_no_permission(self):
        messages.error(self.request,
                       _("You must be logged in to access this page."))
        return redirect(self.login_url)


class ProtectErrorMixin:

    protected_object_url = None
    protected_object_message = _("This object cannot be deleted because it is in use.")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)


class UserPermissionMixin:
    permission_denied_message = "You don't have rights to change another user."
    permission_denied_url = reverse_lazy("users:index")

    def dispatch(self, request, *args, **kwargs):
        # Получаем целевого пользователя (обычно через self.get_object())
        target_user = self.get_object()

        # Проверяем: текущий пользователь == целевой ИЛИ суперпользователь
        if request.user == target_user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Если нет доступа — показываем сообщение и редиректим
        messages.error(request, self.permission_denied_message)
        return redirect(self.permission_denied_url)
