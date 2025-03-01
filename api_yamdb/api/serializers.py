from rest_framework import serializers
from reviews.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import username_validator


class UsernameValidationMixin():
    def validate_username(self, username):
        return username_validator(username)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


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


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления произведения."""
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

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class SignUpSerializer(serializers.Serializer, UsernameValidationMixin):
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH, required=True)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True)


class TokenSerializer(serializers.Serializer, UsernameValidationMixin):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer, UsernameValidationMixin):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверка, что пользователь не оставлял
        отзыв на это произведение ранее."""
        request = self.context.get('request')
        if request.method == 'PATCH':
            return data
        if Review.objects.filter(
                title_id=self.context['view'].kwargs['title_id'],
                author=request.user).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
