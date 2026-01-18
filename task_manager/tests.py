from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            password="adminpass123",
            is_staff=True
        )

    def test_user_creation(self):
        """Тест создания пользователя (C в CRUD)"""
        # Проверяем, что страница регистрации доступна
        response = self.client.get(reverse("users:create"))
        self.assertEqual(response.status_code, 200)
        
        # Создаем пользователя
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "newuser",
                "password1": "newpass123",  # Обрати внимание: password1 и password2
                "password2": "newpass123",
                "email": "new@example.com",
            },
        )

        # Проверяем редирект на страницу входа
        self.assertRedirects(response, reverse("login"))
        
        # Проверяем, что пользователь создался
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login_redirect(self):
        """Тест, что после входа переходим на главную"""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )

        # Проверяем редирект на список пользователей
        self.assertRedirects(response, reverse("users:index"))

    def test_user_update_redirect(self):
        """Тест, что после редактирования переходим на список пользователей"""
        # Входим как администратор (или как сам пользователь)
        self.client.login(username="admin", password="adminpass123")

        response = self.client.post(
            reverse("users:update", args=[self.user.id]),
            {
                "username": "updateduser", 
                "email": "updated@example.com",
                # Добавь другие обязательные поля, если есть
                "first_name": "Test",
                "last_name": "User"
            },
        )

        # Проверяем редирект на список пользователей
        self.assertRedirects(response, reverse("users:index"))

    def test_user_list_no_auth(self):
        """Тест, что список пользователей виден без входа"""
        response = self.client.get(reverse("users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
