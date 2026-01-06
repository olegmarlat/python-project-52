from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserTests(TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.client = Client()

        # Создаем обычного пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Создаем администратора
        self.admin = User.objects.create_user(
            username="admin", password="adminpass123", is_staff=True
        )

    def test_user_creation(self):
        """Тест создания пользователя (C в CRUD)"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password": "newpass123",
                "email": "new@example.com",
            },
        )

        # Проверяем, что после регистрации переходим на страницу входа
        self.assertRedirects(response, reverse("login"))

        # Проверяем, что пользователь создался
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login_redirect(self):
        """Тест, что после входа переходим на главную"""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )

        # Проверяем редирект на главную
        self.assertRedirects(response, reverse("user_list"))

    def test_user_update_redirect(self):
        """Тест, что после редактирования переходим на список пользователей"""
        # Входим как администратор
        self.client.login(username="admin", password="adminpass123")

        response = self.client.post(
            reverse("user_edit", args=[self.user.id]),
            {"username": "updateduser", "email": "updated@example.com"},
        )

        # Проверяем редирект на список пользователей
        self.assertRedirects(response, reverse("user_list"))

    def test_user_list_no_auth(self):
        """Тест, что список пользователей виден без входа"""
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
