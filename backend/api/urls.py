from django.urls import path, re_path, include
from rest_framework import routers
from .views import UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
