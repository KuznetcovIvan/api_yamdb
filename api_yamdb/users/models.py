from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from api.constants import (
    ROLE_MAX_LENGTH, ROLES, USERNAME_MAX_LENGTH,
    BAD_USERNAME, EMAIL_MAX_LENGTH)


class User(AbstractUser):
    email = models.EmailField(
        'Почта', max_length=EMAIL_MAX_LENGTH, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', max_length=ROLE_MAX_LENGTH, choices=ROLES, default='user')
    username = models.CharField(
        'Логин', max_length=USERNAME_MAX_LENGTH, unique=True,
        help_text='Только буквы, цифры и @/./+/-/_',
        validators=(RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Допустимы только буквы, цифры и @/./+/-/_'),)
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=6, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.username == BAD_USERNAME:
            raise ValidationError(
                {'username': f'Имя "{BAD_USERNAME}" запрещено.'})     

    def is_admin(self):
        """Проверяет, является ли пользователь
        администратором."""
        return self.role == 'admin' or self.is_superuser or self.is_staff

    def is_moderator_or_admin(self):
        """Проверяет, является ли пользователь
        модератором или администратором."""
        return (self.role in ('admin', 'moderator')
                or self.is_superuser or self.is_staff)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
