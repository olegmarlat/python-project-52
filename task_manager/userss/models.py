from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})


    def __str__(self):
        return f'{self.username} ({self.email})'
