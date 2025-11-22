from django.urls import path
from task_manager.views import home

urlpatterns = {
    path("", home, name="home"),
}
