# tasks/filters.py
import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task
from statuses.models import Status
from labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Статус",
        empty_label="Любой"
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Исполнитель",
        empty_label="Любой"
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Метка",
        empty_label="Любая"
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Только мои задачи"
    )

    class Meta:
        model = Task
        fields = []

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
