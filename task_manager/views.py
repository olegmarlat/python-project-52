import users
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def trigger_error(request):
    raise Exception("Тестовая ошибка для Rollbar")


def home(request):
    return render(request, 'home.html')


def user_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'users/user_list.html', {'users': users})


"""Регистрация нового пользователя"""


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # проверка на наличие пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь уже существует!")
            return render(request, 'users/register.html')
        # зарегистрируем нового пользователя
        users = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, f'Пользователь {username} зарегистрирован')
        return redirect('login')
    return render(request, users/register.html)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # проверка
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect(user_list)
        else:
            messages.error(request, "Неправильно введены данные!")
    return render(request, users/login.html)


@login_required
def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect(user_list)


# редактирование пользователя
@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_staff and request.user.id != user.id:
        messages.error(request, "Упс, у вас нет прав!")
        return redirect(user_list)
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        if request.user.is_staff:
            user.is_staff = 'is_staff' in request.POST
            user.is_active = 'is_active' in request.POST
        # смена пароля, если указан новый
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, f'Данные  {user.username} обновлены!')
        return redirect('user_list')
    return render(request, 'users/user_edit.html', {'user': user})


@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_staff:
        messages.error(request, "У вас нет прав для удаления пользователей!")
        return redirect('user_list')
    if request.user.id == user.id:
        messages.error(request, 'Вы не можете удалить свой аккаунт')
        return redirect('user_list')
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Пользователь {username} удалён!')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})
