from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from django.contrib.messages import success
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings


@receiver(user_logged_in)
def show_login_message(sender, request, user, **kwargs):
    if settings.TESTING:
        return
    success(request, _("Вы залогинены"))


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_manager.users"
