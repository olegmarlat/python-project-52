from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    task_update,
    task_delete,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks_list"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("<int:pk>/update/", task_update, name="update"),
    path("<int:pk>/delete/", task_delete, name="delete"),
]
