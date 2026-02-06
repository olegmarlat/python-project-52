from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersIndexView.as_view(), name='index'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    # path('create/', views.UserCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
]
