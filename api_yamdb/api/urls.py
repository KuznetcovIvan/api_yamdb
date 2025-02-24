from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryViewSet, GenreViewSet

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    #path('v1/auth/signup/', include('djoser.urls.jwt')),
    #path('v1/auth/token/', ),
    #path('v1/users/me/', ),
    #path('v1/users/signup/', include('djoser.urls.jwt')),
]
