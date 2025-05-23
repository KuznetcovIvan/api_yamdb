from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Category, Genre)
class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    search_fields = ('title__name', 'author__username')
    list_filter = ('score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'pub_date')
    search_fields = ('review__title__name', 'author__username')
    list_filter = ('pub_date',)


UserAdmin.fieldsets += (('О пользователе', {'fields': ('bio', 'role')}),)

admin.site.register(User, UserAdmin)
