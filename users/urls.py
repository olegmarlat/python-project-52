from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    # path('', views.user_list, name='user_list'),
    path('', views.index, name='index'),
    # path('', include('users.urls')),
    # path('profile/', views.profile, name='profile'),
    # path('users/', views.user_list, name='user_list'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    # path('users/<int:user_id>/delete/', views.user_delete, name='user_delete
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
    path('profile/', views.profile, name='profile'),
]
