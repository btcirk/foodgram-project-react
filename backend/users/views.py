from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from djoser.views import UserViewSet as djoserUserViewSet

from .models import User, Follow
from .serializers import UserSerializer, FollowSerializer
from .permissions import OnlyAuthenticated


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class UserViewSet(djoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, url_path='me', methods=['get'],
            permission_classes=[OnlyAuthenticated]
            )
    def me(self, request):
        user = User.objects.get(username=request.user)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#class UsersViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

#    def get_queryset(self):
#        user = self.request.user
#        queryset = super().get_queryset()
#        if self.action == "detail":
#            queryset = queryset.filter(pk=user.pk)
#        return queryset