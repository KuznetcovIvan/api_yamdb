from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class MyUser(AbstractUser):
    email = models.EmailField('Почта', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', max_length=10, choices=CHOICES, default='user')
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)

    def __str__(self):
        return self.username
