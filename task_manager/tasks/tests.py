from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="123")
        self.user2 = User.objects.create_user(username="bob", password="123")
        self.status = Status.objects.create(name="В работе")
        self.client.login(username="alice", password="123")

    def test_create_task(self):
        response = self.client.post(
            reverse("task_create"),
            {"name": "Новая задача", "status": self.status.id},
        )
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.author, self.user1)
        self.assertRedirects(response, reverse("tasks_list"))

    def test_delete_own_task(self):
        task = Task.objects.create(
            name="Моя задача", author=self.user1, status=self.status
        )
        response = self.client.post(reverse("task_delete", args=[task.pk]))
        self.assertEqual(Task.objects.count(), 0)

        self.assertRedirects(response, reverse("tasks_list"))

    def test_cannot_delete_other_user_task(self):
        task = Task.objects.create(
            name="Чужая задача", author=self.user2, status=self.status
        )
        response = self.client.post(reverse("task_delete", args=[task.pk]))
        self.assertEqual(Task.objects.count(), 1)
        self.assertRedirects(response, reverse("tasks_list"))


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="123")
        self.user2 = User.objects.create_user(username="bob", password="123")
        self.status_new = Status.objects.create(name="Новый")
        self.status_in_progress = Status.objects.create(name="В работе")
        self.label_bug = Label.objects.create(name="Баг")

        self.task1 = Task.objects.create(
            name="Задача 1",
            author=self.user1,
            status=self.status_new,
        )
        self.task1.labels.add(self.label_bug)

        self.task2 = Task.objects.create(
            name="Задача 2",
            author=self.user2,
            status=self.status_in_progress,
        )

        self.client.login(username="alice", password="123")

    def test_filter_by_status(self):
        response = self.client.get(
            reverse("tasks_list"),
            {"status": self.status_new.id}
        )
        self.assertContains(response, "Задача 1")
        self.assertNotContains(response, "Задача 2")

    def test_filter_by_label(self):

        response = self.client.get(
            reverse("tasks_list"),
            {"labels": self.label_bug.id}
        )
        self.assertContains(response, "Задача 1")
        self.assertNotContains(response, "Задача 2")

    def test_filter_self_tasks(self):
        response = self.client.get(reverse("tasks_list"), {"self_tasks": "on"})
        self.assertContains(response, "Задача 1")
        self.assertNotContains(response, "Задача 2")

    def test_combined_filters(self):
        response = self.client.get(
            reverse("tasks_list"),
            {"status": self.status_new.id, "self_tasks": "on"},
        )
        self.assertContains(response, "Задача 1")
        self.assertNotContains(response, "Задача 2")
