from django.urls import path, include
from rest_framework import routers

#from ..users.views import UsersViewSet


urlpatterns = [
    #path('', include(router.urls)),
    path('auth/', include('users.urls')),
    path('users/', include('users.urls')),
]
