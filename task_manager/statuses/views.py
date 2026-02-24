from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Status
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class StatusListView(ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CreateView):
    model = Status
    template_name = 'statuses/status_create.html'
    fields = ['name']
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Статус успешно создан')
        return response


class StatusUpdateView(UpdateView):
    model = Status
    template_name = 'statuses/status_update.html'
    fields = ['name']
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Статус успешно изменен')
        return response


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses_list')

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(self.request, "Статус успешно удален")
            return response
        except ProtectedError:
            messages.error(
                self.request,
                "Невозможно удалить статус, потому что он используется"
            )
            return redirect('statuses_list')

