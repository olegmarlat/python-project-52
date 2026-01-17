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
    ProtectErrorMixin,
)
from django.contrib import messages
from django.shortcuts import redirect


LABELS_INDEX_URL = 'labels:index'


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"
    ordering = ["id"]


class LabelCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Label
    template_name = "labels/label_form.html"
    form_class = LabelCreationForm
    success_url = reverse_lazy(LABELS_INDEX_URL)
    success_message = _("Label was created successfully")
    extra_context = {"title": _("Create label"), "button_name": _("Create")}


class LabelUpdateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = LabelCreationForm
    model = Label
    template_name = "labels/label_form.html"
    success_url = reverse_lazy(LABELS_INDEX_URL)
    success_message = _("Label was updated successfully")
    extra_context = {"title": _("Update label"), "button_name": _("Update")}


class LabelDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    ProtectErrorMixin,
    DeleteView,
):
    template_name = "labels/label_delete.html"
    model = Label
    success_url = reverse_lazy(LABELS_INDEX_URL)
    success_message = _("Label was deleted successfully")
    protected_object_url = reverse_lazy(LABELS_INDEX_URL)
    protected_object_message = _(
        "Cannot delete this label because it is being used"
    )
    extra_context = {
        "title": _("Label deletion"),
        "button_name": _("Yes, delete"),
    }
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 🔥 Проверяем, используется ли метка в задачах
        if self.object.task_set.exists():
            messages.error(request, "Невозможно удалить метку, потому что она используется")
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
