from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


# creating a class for CRUD


class UserTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.client.force_login(self.user)

    def test_create_user(self):
        response = self.client.post(
            reverse("user_create"),
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
        user = User.objects.get(pk=2)
        response = self.client.post(
            reverse("user_update", kwargs={"pk": self.user.pk}),
            {
                "first_name": "TestName",
                "last_name": user.last_name,
                "username": user.username,
            },
        )
        user.refresh_from_db()
        self.assertEqual(user.first_name, "TestName")
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        user = User.objects.get(pk=2)
        response = self.client.post(
            reverse(
                "user_delete",
                kwargs={
                    "pk": user.pk,
                },
            )
        )
        self.assertFalse(User.objects.filter(pk=2).exists())
        self.assertEqual(response.status_code, 302)


"""


    # Create
    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'alice')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.check_password('secret123'))

    #  Update
    def test_update_user(self):
        user = User.objects.create_user(**self.user_data)
        user.phone_number = '+0987654321'
        user.save()
        updated_user = User.objects.get(username='alice')
        self.assertEqual(updated_user.phone_number, '+0987654321')

    # Delete
    def test_delete_user(self):
        user = User.objects.create_user(**self.user_data)
        user_id = user.id
        user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)"""
