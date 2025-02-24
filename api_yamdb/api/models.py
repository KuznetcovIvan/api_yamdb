from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Category(models.Model):
    """Категории."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(datetime.datetime.now().year)],
        help_text='Нельзя добавлять произведения, которые еще не вышли. Год выпуска не может быть больше текущего.'
    )
    rating = models.IntegerField(
        null=True, blank=True,
        help_text='Рейтинг.'
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles')

    def __str__(self):
        return self.name
