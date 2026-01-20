
from django.contrib import admin
from django.urls import path, include
from . import views
from task_manager.users.views import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("labels/", include("task_manager.labels.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("test-rollbar/", views.trigger_error),
    path("login/", CustomLoginView.as_view(), name="login"),
]
