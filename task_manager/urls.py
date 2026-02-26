from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from task_manager.users.views import (
    UserCreateView,
    UserLogoutView,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("admin/", admin.site.urls),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("users/create/", UserCreateView.as_view(), name="register"),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("labels/", include("task_manager.labels.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='users/login.html',
             redirect_authenticated_user=True
         ),
         name='login'),
]
