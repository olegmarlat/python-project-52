from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.db.models import Q
from task_manager.tasks.models import Task
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from task_manager.mixins import (
    LoginRequiredMessageMixin,
    ProtectedObjectMixin,
)

User = get_user_model()

USERS_INDEX_URL = "users:index"


class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "users/registration_form.html"
    success_url = reverse_lazy("login")
    success_message = _("Пользователь успешно зарегистрирован")
    extra_context = {
        "title": _("Регистрация"),
        "button_text": _("Зарегистрироваться"),
    }

    def get_form_class(self):
        from .forms import UserCreationForm
        return UserCreationForm


class UserLoginView(LoginRequiredMessageMixin,
                    SuccessMessageMixin, CreateView):
    template_name = "users/login.html"
    success_url = reverse_lazy("index")
    success_message = _("Вы залогинены")
    extra_context = {
        "title": _("Вход"),
        "button_text": _("Войти"),
    }

    def get_form_class(self):
        from django.contrib.auth.forms import AuthenticationForm
        return AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _("Вы залогинены"))
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        was_authenticated = request.user.is_authenticated
        logout(request)
        if was_authenticated:
            messages.success(request, _("Вы разлогинены"))
        return redirect("index")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = User
    template_name = "users/user_edit.html"
    success_url = reverse_lazy(USERS_INDEX_URL)
    success_message = _("Пользователь успешно изменен")
    permission_denied_message = _(
        "У вас нет прав для изменения другого пользователя."
    )
    extra_context = {
        "title": _("Редактировать профиль"),
        "button_text": _("Изменить"),
    }

    def get_form_class(self):
        from .forms import UserUpdateForm
        return UserUpdateForm
from django.db.models import ProtectedError



class UserDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("users:index")
    success_message = _("Пользователь успешно удален")
    extra_context = {
        "title": _("Удаление пользователя"),
        "button_text": _("Да, удалить"),
    }
    """проба """
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

    
    """ def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        
        if Task.objects.filter(Q(author=user) | Q(executor=user)).exists():
            messages.error(
                request,
                _("Невозможно удалить пользователя, потому что он используется")
            )
            return redirect(reverse_lazy('users'))
            # return redirect(self.success_url)
        
        return super().dispatch(request, *args, **kwargs)"""
    
        def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        
        if Task.objects.filter(Q(author=user) | Q(executor=user)).exists():
            messages.error(
                request,
                _("Невозможно удалить пользователя, потому что он используется")
            )

            return redirect(reverse_lazy('users:index'))

        if request.method == 'GET':
            return self.post(request, *args, **kwargs)
            
        return super().dispatch(request, *args, **kwargs)

