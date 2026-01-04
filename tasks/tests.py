from django.test import TestCase

# Create your tests here.
# tasks/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from statuses.models import Status

class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='123')
        self.user2 = User.objects.create_user(username='bob', password='123')
        self.status = Status.objects.create(name='В работе')
        self.client.login(username='alice', password='123')

    def test_create_task(self):
        response = self.client.post(reverse('task_create'), {
            'name': 'Новая задача',
            'status': self.status.id
        })
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.author, self.user1)
        self.assertRedirects(response, reverse('tasks_list'))

    def test_delete_own_task(self):
        task = Task.objects.create(name='Моя задача', author=self.user1, status=self.status)
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, reverse('tasks_list'))

    def test_cannot_delete_other_user_task(self):
        task = Task.objects.create(name='Чужая задача', author=self.user2, status=self.status)
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(Task.objects.count(), 1)  # задача НЕ удалена
        self.assertRedirects(response, reverse('tasks_list'))
