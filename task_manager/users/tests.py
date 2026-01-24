from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.client.force_login(self.user)

    def test_create_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Darya",
                "last_name": "Star",
                "username": "daryastar",
                "password1": "WordPass123",
                "password2": "WordPass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="daryastar").exists())

    def test_update_user(self):
        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.user.pk}),
            {
                "first_name": "TestName",
                "last_name": self.user.last_name,
                "username": self.user.username,
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "TestName")
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        response = self.client.post(
            reverse("users:delete", kwargs={"pk": self.user.pk})
        )
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertEqual(response.status_code, 302)
