from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin", password="adminpass123", is_staff=True
        )

    def test_user_creation(self):
        """Тест создания пользователя (C в CRUD)"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "password1": "newpass123",
                "password2": "newpass123",
                "email": "new@example.com",
            },
        )
        self.assertRedirects(response, reverse("login"))

        # проверка создания пользователя
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login_redirect(self):
        """проверка, что после входа переходим на главную"""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertRedirects(response, reverse("users:index"))

    def test_user_update_redirect(self):
        """После редактирования переходим на список пользователей"""
        self.client.login(username="admin", password="adminpass123")

        response = self.client.post(
            reverse("users:update", args=[self.user.id]),
            {
                "username": "updateduser",
                "email": "updated@example.com",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        self.assertRedirects(response, reverse("users:index"))

    def test_user_list_no_auth(self):
        """Тест, что список пользователей виден без входа"""
        response = self.client.get(reverse("users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
