from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.timezone import now

from api.constants import (
    MAX_LENGTH_NAME, MAX_LENGTH_SLUG, MAX_LENGTH_STR,
    MIN_SCORE, MAX_SCORE
)


def validate_year(year):
    """Проверка года."""
    current_year = now().year
    if year > current_year:
        raise ValidationError(
            f'Год не может быть больше текущего ({current_year})'
        )
    return year


class SlugNameBaseModel(models.Model):
    """Базовая слаг модель."""
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг'
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
        default_related_name = 'titles'


class Genre(SlugNameBaseModel):
    """Жанр."""
    class Meta(SlugNameBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'titles'


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        validators=[validate_year]
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    @property
    def rating(self):
        """Вычисляет средний рейтинг произведения на основе отзывов."""
        result = self.reviews.aggregate(Avg('score'))
        return result['score__avg']

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name',)

    def __str__(self):
        return f'{self.name[:MAX_LENGTH_STR]}, {self.year} года.'


class BaseReviewComment(models.Model):
    """Базовый класс для отзывов и комментариев."""
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_related',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author} - {self.text[:20]}'


class Review(BaseReviewComment):
    """Отзывы на произведения."""
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'


class Comment(BaseReviewComment):
    """Комментарии к отзывам."""
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review}'