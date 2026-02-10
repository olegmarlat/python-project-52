# tasks/filters.py
import django_filters
from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Статус",
        empty_label="Любой",
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Исполнитель",
        empty_label="Любой",
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Метка",
        empty_label="Любая",
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
