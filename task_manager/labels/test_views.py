from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.test import TestCase
from task_manager.users.models import User
from task_manager.statuses.models import Status


class LabelTestCase(TestCase):
    def setUp(self):
        # Создаём пользователей
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password456',
            first_name='User',
            last_name='Two'
        )

        # Создаём статус (нужен для задачи в test_cannot_delete_label_in_use)
        self.status = Status.objects.create(name="Новый")

        # Создаём метки
        self.label1 = Label.objects.create(name="Метка 1")
        self.label2 = Label.objects.create(name="Метка 2")

        # Считаем количество меток
        self.label_count = Label.objects.count()

        # Данные для создания и обновления метки
        self.valid_label_data = {"name": "Новая метка"}
        self.update_label_data = {"name": "Обновлённая метка"}


class TestLabelListView(LabelTestCase):
    def test_labels_list_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)

        # Исправлено: labels:index → labels_list
        response = self.client.get(reverse_lazy("labels_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/index.html")
        self.assertEqual(Label.objects.count(), self.label_count)

    def test_labels_list_unauthorized(self):
        # Исправлено: labels:index → labels_list
        response = self.client.get(reverse_lazy("labels_list"))
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)


class TestLabelCreateView(LabelTestCase):
    def test_label_creation_authorized(self):
        user1 = self.user1
        label_data = self.valid_label_data
        self.client.force_login(user1)
        initial_count = Label.objects.count()

        # Исправлено: labels:create → labels_create
        response = self.client.get(reverse_lazy("labels_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_form.html")

        response = self.client.post(
            reverse_lazy("labels_create"),
            data=label_data,
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: labels:index → labels_list
        self.assertRedirects(response, reverse_lazy("labels_list"))
        self.assertEqual(Label.objects.count(), initial_count + 1)

    def test_label_creation_unauthorized(self):
        label_data = self.valid_label_data

        # Исправлено: labels:create → labels_create
        response = self.client.get(reverse_lazy("labels_create"))
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)

        response = self.client.post(
            reverse_lazy("labels_create"),
            data=label_data,
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)


class TestLabelUpdateView(LabelTestCase):
    def test_label_update_authorized(self):
        user1 = self.user1
        label1 = self.label1
        update_data = self.update_label_data
        self.client.force_login(user1)

        # Исправлено: labels:update → labels_update
        response = self.client.get(
            reverse_lazy("labels_update", kwargs={"pk": label1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_form.html")

        response = self.client.post(
            reverse_lazy("labels_update", kwargs={"pk": label1.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: labels:index → labels_list
        self.assertRedirects(response, reverse_lazy("labels_list"))
        updated_label = Label.objects.get(id=label1.id)
        self.assertEqual(updated_label.name, update_data["name"])

    def test_label_update_unauthorized(self):
        label1 = self.label1
        update_data = self.update_label_data

        # Исправлено: labels:update → labels_update
        response = self.client.get(
            reverse_lazy("labels_update", kwargs={"pk": label1.id})
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)

        response = self.client.post(
            reverse_lazy("labels_update", kwargs={"pk": label1.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)


class TestLabelDeleteView(LabelTestCase):
    def test_label_deletion_authorized(self):
        user1 = self.user1
        label1 = self.label1
        self.client.force_login(user1)
        initial_count = Label.objects.count()

        # Исправлено: labels:delete → labels_delete
        response = self.client.get(
            reverse_lazy("labels_delete", kwargs={"pk": label1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_delete.html")

        response = self.client.post(
            reverse_lazy("labels_delete", kwargs={"pk": label1.id})
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: labels:index → labels_list
        self.assertRedirects(response, reverse_lazy("labels_list"))
        self.assertEqual(Label.objects.count(), initial_count - 1)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=label1.id)

    def test_label_deletion_unauthorized(self):
        label1 = self.label1

        # Исправлено: labels:delete → labels_delete
        response = self.client.get(
            reverse_lazy("labels_delete", kwargs={"pk": label1.id})
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)

        response = self.client.post(
            reverse_lazy("labels_delete", kwargs={"pk": label1.id})
        )
        self.assertEqual(response.status_code, 302)
        # Исправлено: добавлен fetch_redirect_response=False
        self.assertRedirects(response, '/login/',
                             fetch_redirect_response=False)

    def test_cannot_delete_label_in_use(self):
        task = Task.objects.create(
            name="Задача",
            author=self.user1,
            status=self.status,
        )
        task.labels.add(self.label1)

        self.client.force_login(self.user1)
        # Исправлено: labels:delete → labels_delete
        response = self.client.post(
            reverse_lazy("labels_delete", kwargs={"pk": self.label1.id})
        )

        self.assertEqual(Label.objects.count(), 2)
        self.assertTrue(Label.objects.filter(id=self.label1.id).exists())
        # проверка перенаправления
        self.assertEqual(response.status_code, 302)
        # Исправлено: labels:index → labels_list
        self.assertRedirects(response, reverse_lazy("labels_list"))
