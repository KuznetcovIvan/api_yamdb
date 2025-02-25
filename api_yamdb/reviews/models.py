from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import datetime


class Category(models.Model):
    """Категории."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(datetime.datetime.now().year)],
        help_text='Год выпуска не может быть больше текущего.'
    )
    rating = models.IntegerField(
        null=True, blank=True,
        help_text='Рейтинг.'
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles')

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')
        ordering = ['-pub_date']

    def __str__(self):
        return f'Review by {self.author} on {self.title}'


class Comment(models.Model):
    """Комментарии к отзывам."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f'Comment by {self.author} on review {self.review.id}'
