from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import ListView, DeleteView


def index(request):
    return HttpResponse("Users app is working!")


def profile(request):
    return HttpResponse("User profile page")


# Views для аутентификации
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


# View для регистрации
class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


# View для обновления профиля (используем стандартную форму)
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user


# Create your views here.
