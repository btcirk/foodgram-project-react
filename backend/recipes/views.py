import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Ingredient, Recipe, Favorites, Cart, IngredientAmount
from .serializers import TagSerializer, IngredientSerializer
from .serializers import RecipeSerializer, RecipeMiniSerializer
from .filters import RecipeFilter, IngredientsFilter
from .permissions import Owner
from api.pagination import LimitPageNumberPagination


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    pagination_class = None


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if (self.action == 'partial_update' or self.action == 'destroy'):
            return (Owner(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeMiniSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Favorites, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorites, request.user, pk)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Cart, request.user, pk)
        return None

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        i_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in i_list:
                i_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                i_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('OpenSans', 'OpenSans-Regular.ttf', 'UTF-8'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont('OpenSans', size=24)
        p.drawString(200, 800, 'Список ингредиентов')
        p.setFont('OpenSans', size=16)
        height = 750
        for item in i_list:
            p.drawString(75, height, (f'- {item} '
                                      f'({i_list[item]["measurement_unit"]})'
                                      f' - {i_list[item]["amount"]}'))
            height -= 25
        p.drawString(100, 100, "Hello world.")
        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='ingredients_list.pdf')
