from django.urls import path
from . import views

urlpatterns = [
    path('', views.statuses_list, name='statuses_list'),
    path('create/', views.status_create, name='status_create'),
    path('update/<int:pk>/', views.status_update, name='status_update'),
    path('delete/<int:pk>/', views.status_delete, name='status_delete'),
]
