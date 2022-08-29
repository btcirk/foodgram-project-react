from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import AllowAny
from .models import Tag
from .serializers import TagSerializer


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny,]
    pagination_class = None
