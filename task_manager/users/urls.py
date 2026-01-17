from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='index'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
    path('login/', LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/',LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
]
