from django.urls import path
from .views import (
    TaskListView,
    task_create,
    task_update,
    task_delete,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="index"),  # ← index вместо tasks_list
    path("create/", task_create, name="create"),
    path("<int:pk>/update/", task_update, name="update"),
    path("<int:pk>/delete/", task_delete, name="delete"),
]
