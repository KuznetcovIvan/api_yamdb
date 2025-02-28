from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from api.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from api.validators import username_validator


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'category', 'genre'
        )


class TitleReadSerializer(serializers.ModelSerializer):
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
        read_only_fields = fields


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH, required=True)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True)

    def validate_username(self, username):
        return username_validator(username)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True)
    confirmation_code = serializers.CharField()

    def validate_username(self, username):
        return username_validator(username)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, username):
        return username_validator(username)


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


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
