from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Label

# task_manager/labels/views.py


class MyLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для редиректа на логин без параметра ?next="""
    def handle_no_permission(self):
        messages.error(self.request,
                       'Вы не авторизованы! Пожалуйста, войдите.')
        return redirect('login')


class LabelListView(MyLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'


class LabelCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно создана'


class LabelUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(MyLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(
                self.request,
                'Невозможно удалить метку, так как она используется')
            return redirect('label_list')
        return super().post(request, *args, **kwargs)

    """
class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно создана'


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверяем, есть ли задачи, использующие эту метку
        if self.object.task_set.exists():
            messages.error(self.request, 'Невозможно удалить метку')
            return redirect('label_list')
        return super().post(request, *args, **kwargs)
        """
