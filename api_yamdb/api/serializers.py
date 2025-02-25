import re

from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'category', 'genre')


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

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {'username': 'Это имя уже занято.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Этот email уже занят.'})
        return data


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
        return username

class MeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta(UserSerializer.Meta):
        pass