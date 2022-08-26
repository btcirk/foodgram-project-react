from django.urls import path, re_path, include
from rest_framework import routers
from djoser.views import UserViewSet


urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'list'}), name='user'),
    path('users/set_password/', UserViewSet.as_view({'post': 'set_password'}), name='set_password'),
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name='me'),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
