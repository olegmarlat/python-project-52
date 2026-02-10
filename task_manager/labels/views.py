from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Label


class LabelListView(ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(CreateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Метка успешно создана')
        return response


class LabelUpdateView(UpdateView):
    model = Label
    template_name = 'labels/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Метка успешно изменена')
        return response


class LabelDeleteView(DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Метка успешно удалена')
        return response
