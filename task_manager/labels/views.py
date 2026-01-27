from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from .forms import LabelCreationForm
from .models import Label
from task_manager.mixins import (
    CustomLoginRequiredMixin,
)
from django.contrib import messages
from django.shortcuts import redirect

LABELS_INDEX_URL = "labels:index"


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"
    ordering = ["id"]


class LabelCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Label
    template_name = "labels/label_form.html"
    form_class = LabelCreationForm
    success_url = reverse_lazy(LABELS_INDEX_URL)
    success_message = _("Метка успешно создана")  # Исправлено!
    extra_context = {"title": _("Создать метку"),
                     "button_name": _("Создать")}


class LabelUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    form_class = LabelCreationForm
    model = Label
    template_name = "labels/label_form.html"
    success_url = reverse_lazy(LABELS_INDEX_URL)
    success_message = _("Метка успешно изменена")
    extra_context = {"title": _("Редактировать метку"),
                     "button_name": _("Изменить")}


class LabelDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "labels/label_delete.html"
    model = Label
    success_url = reverse_lazy(LABELS_INDEX_URL)
    success_message = _("Метка успешно удалена")
    extra_context = {
        "title": _("Удаление метки"),
        "button_name": _("Да, удалить"),
    }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        from task_manager.tasks.models import Task

        if Task.objects.filter(labels=self.object).exists():
            messages.error(
                request,
                _("Невозможно удалить метку, потому что она используется")
            )
            return redirect(self.success_url)

        # Если метку можно удалить — вызываем родительский post
        return super().post(request, *args, **kwargs)
