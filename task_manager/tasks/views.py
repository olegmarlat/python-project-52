from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import TaskFilter


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, "Задача успешно создана!")
            return redirect("tasks_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, "Вы не можете редактировать чужую задачу.")
        return redirect("tasks_list")
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Задача успешно изменена!")
            return redirect("tasks_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, "Вы не можете удалить чужую задачу!")
        return redirect("tasks_list")
    if request.method == "POST":
        task.delete()
        messages.success(request, "Задача успешно удалена!")
        return redirect("tasks_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Task.objects.all()
        self.filterset = TaskFilter(
            self.request.GET,
            queryset=queryset,
            request=self.request,
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = (
            self.filterset
        )  # чтобы отобразить форму в шаблоне
        return context
