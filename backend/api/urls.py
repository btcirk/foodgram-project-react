from django.urls import path, re_path, include
from rest_framework import routers
from users.views import UserViewSet
from recipies.views import TagViewSet, IngredientViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='tags')
#router.register(r'users/me', UserViewSet, basename='me')
#router.register(r'users/set_password', UserViewSet, basename='set-password')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    #path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    #path('users/<int:pk>/', UserViewSet.as_view({'get': 'list'}), name='user'),
    #path('users/set_password/', UserViewSet.as_view({'post': 'set_password'}), name='set_password'),
    #path('users/me/', UsersViewSet.as_view({'get': 'me'}), name='me'),
    #re_path('', include('djoser.urls')),
]
