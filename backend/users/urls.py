from django.urls import include, path
from rest_framework import routers

from .views import get_token, delete_token
from .views import UsersViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('token/login/', get_token, name='login'),
    path('token/logout/', delete_token, name='logout'),
    #path('', include(router.urls)),
]