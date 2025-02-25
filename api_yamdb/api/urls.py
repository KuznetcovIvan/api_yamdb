from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    SignUpViewSet, TokenViewSet)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')

v1_router.register('auth/signup', SignUpViewSet, basename='signup')
v1_router.register('auth/token', TokenViewSet, basename='token')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
