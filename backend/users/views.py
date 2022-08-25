from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import TokenSerializer


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        return Response('OK', status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def delete_token(request):
    return Response('OK', status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    pass
