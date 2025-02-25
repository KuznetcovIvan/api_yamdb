from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, SignUpViewSet,
    TitleViewSet, TokenViewSet, UserViewSet,)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')

v1_router.register('auth/signup', SignUpViewSet, basename='signup')
v1_router.register('auth/token', TokenViewSet, basename='token')
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
