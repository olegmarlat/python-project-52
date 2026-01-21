from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from task_manager.users.views import UserCreateView, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # Глобальные маршруты аутентификации
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),

    # Остальные приложения
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('test-rollbar/', views.trigger_error),
]
