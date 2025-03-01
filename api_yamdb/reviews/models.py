from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (EMAIL_MAX_LENGTH, MAX_LENGTH_NAME, MAX_LENGTH_SLUG,
                        MAX_LENGTH_STR, MAX_SCORE, MIN_SCORE, ROLE_ADMIN,
                        ROLE_MODERATOR, ROLE_USER, USERNAME_MAX_LENGTH)
from .validators import username_validator, validate_year

ROLES = (
    (ROLE_USER, 'Аутентифицированный пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)


class SlugNameBaseModel(models.Model):
    """Базовая модель с полями name и slug."""
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(SlugNameBaseModel):
    """Категория."""

    class Meta(SlugNameBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(SlugNameBaseModel):
    """Жанр."""

    class Meta(SlugNameBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название',
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[validate_year],
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')
        default_related_name = 'titles'

    def __str__(self):
        return f'{self.name[:MAX_LENGTH_STR]}, {self.year} года.'


class TextContent(models.Model):
    """Mодель для текстового контента с автором и датой публикации."""
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='%(class)s_related'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = 'texts'

    def __str__(self):
        return f'{self.author} - {self.text[:20]}'


class Review(TextContent):
    """Отзывы на произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(
            MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        verbose_name='Оценка'
    )

    class Meta(TextContent.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'


class Comment(TextContent):
    """Комментарии к отзывам."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta(TextContent.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review}'


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=ROLE_USER,
    )
    username = models.CharField(
        'Логин',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Только буквы, цифры и @/./+/-/_',
        validators=(username_validator,)
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True,
    )

    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == ROLE_ADMIN or self.is_staff

    def is_moderator(self):
        """Проверяет, является ли пользователь модератором. """
        return self.role == ROLE_MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
