from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import ProtectedError  # ← ОБЯЗАТЕЛЬНО!
from .models import Status
from .forms import StatusForm
from django.contrib.auth.decorators import login_required


@login_required
def statuses_list(request):
    statuses = Status.objects.all()
    return render(
        request, "statuses/statuses_list.html", {"statuses": statuses}
    )


@login_required
def status_create(request):
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно создан!")
            return redirect("statuses:statuses_list")
    else:
        form = StatusForm()
    return render(request, "statuses/status_form.html", {"form": form})


@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно изменен!")
            return redirect("statuses:statuses_list")
    else:
        form = StatusForm(instance=status)
    return render(request, "statuses/status_form.html", {"form": form})


@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        try:
            status.delete()
            messages.success(request, "Статус успешно удален!")
            return redirect("statuses:statuses_list")
        except ProtectedError:
            messages.error(request, "Невозможно удалить статус")
            return redirect("statuses:statuses_list")
    return render(
        request, "statuses/status_confirm_delete.html", {"status": status}
    )
