from django.urls import path
from . import views

app_name = 'statuses'

urlpatterns = [
    path("", views.statuses_list, name="statuses_list"),
    # path("create/", views.status_create, name="create"),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path("<int:pk>/update/", views.status_update, name="update"),
    path("<int:pk>/delete/", views.status_delete, name="delete"),
]
