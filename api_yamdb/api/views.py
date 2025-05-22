from random import choices

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CurrentUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleCreateUpdateSerializer, TitleReadSerializer,
                          TokenSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by(*Title._meta.ordering)
    serializer_class = TitleReadSerializer
    pagination_class = PageNumberPagination
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleCreateUpdateSerializer

    def perform_create(self, serializer):
        """Создание нового произведения."""
        serializer.save()


class BaseSlugViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Базовый вьюсет для категорий и жанров."""
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(BaseSlugViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseSlugViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    """Регистрирует нового пользователя и
    отправляет проверочный код на email."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise ValidationError(
            {'email': 'email уже занят.'}
            if User.objects.filter(
                email=serializer.validated_data['email']).exists()
            else {'username': 'username уже занят.'}
        )

    confirmation_code = ''.join(choices(
        settings.CONFIRMATION_CODE_CHARS,
        k=settings.CONFIRMATION_CODE_LENGTH))
    user.confirmation_code = confirmation_code
    user.save(update_fields=['confirmation_code'])

    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        recipient_list=(user.email,),
        from_email=None,
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    """Выдаёт JWT-токен после проверки электронной почты."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'])
    if (user.confirmation_code
       != serializer.validated_data['confirmation_code']
       or user.confirmation_code == settings.BLOCKED_PIN):
        raise ValidationError(
            {'confirmation_code': 'Неверный код подтверждения'})
    if user.confirmation_code != settings.BLOCKED_PIN:
        user.confirmation_code = settings.BLOCKED_PIN
        user.save(update_fields=['confirmation_code'])
    return Response(
        {'token': str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK,
    )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdmin,)

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path=settings.PROFILE_URL_SEGMENT,
        permission_classes=(IsAuthenticated,),
        serializer_class=CurrentUserSerializer,
    )
    def current_user(self, request):
        """Обрабатывает запросы к профилю текущего пользователя."""
        user = request.user
        if request.method != 'PATCH':
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        serializer = CurrentUserSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorOrAdminOrReadOnly,
    )

    def get_title(self):
        """Получает объект Title по title_id из URL."""
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        """Возвращает queryset с отзывами для конкретного title."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для конкретного title."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorOrAdminOrReadOnly,
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        """Получает объект Review по review_id из URL."""
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        """Возвращает queryset с комментариями для конкретного review."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для конкретного review."""
        serializer.save(author=self.request.user, review=self.get_review())
