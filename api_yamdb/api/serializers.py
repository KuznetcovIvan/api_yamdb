import datetime
import re

from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления произведения."""
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведения."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title

        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'category', 'genre'
        )


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Имя "me" запрещено.')
        if not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
                'Допустимы только буквы, цифры и @/./+/-/_')
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Имя "me" запрещено.')
        if not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
                'Допустимы только буквы, цифры и @/./+/-/_')
        return username


class MeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta(UserSerializer.Meta):
        pass


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    text = serializers.CharField(max_length=1000)
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    text = serializers.CharField(max_length=1000)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
