from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from task_manager.users.views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("admin/", admin.site.urls),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("users/create/", UserCreateView.as_view(), name="register"),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls", namespace="statuses")),
    path("labels/", include("task_manager.labels.urls", namespace="labels")),
    path("tasks/", include("task_manager.tasks.urls")),
]