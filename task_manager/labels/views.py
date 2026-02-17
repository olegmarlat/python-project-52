from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from .models import Label

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('labels:label_list')
    success_message = 'Метка успешно создана'

class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('labels:label_list')
    success_message = 'Метка успешно изменена'

class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить метку, потому что она используется')
            return redirect('labels:label_list')
