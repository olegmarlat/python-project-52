from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def handle_no_permission(self):
        messages.error(self.request, "You must be logged in to access this page.")
        return redirect(self.login_url)


class ProtectErrorMixin:
    """Миксин для перехвата ошибки IntegrityError при удалении защищённого объекта."""
    protected_object_url = None
    protected_object_message = "This object cannot be deleted because it is in use."

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)
