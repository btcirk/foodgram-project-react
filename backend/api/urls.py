from django.urls import path, re_path, include
from rest_framework import routers


urlpatterns = [
    path('', include('djoser.urls.base')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
