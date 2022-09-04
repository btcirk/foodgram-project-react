import os.path
from foodgram.settings import MEDIA_ROOT

from rest_framework import viewsets, mixins, status, filters
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

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from django.http import HttpResponse
import uuid


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

    def generate_pdf(self, shopping_list):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        for item in shopping_list:
            str = f'{item} ({shopping_list[item]["measurement_unit"]}) - {shopping_list[item]["amount"]}'
            layout.add(UnorderedList().add(Paragraph(str, font="Courier")))
        filename = str(uuid.uuid4())
        full_path = os.path.join(MEDIA_ROOT, filename)
        print(full_path)
        #with open(filename, "wb") as pdf_file_handle:
        #    PDF.dumps(pdf_file_handle, doc)
        return filename

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in ingredients_list:
                ingredients_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                ingredients_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('OpenSans', 'OpenSans-Regular.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('OpenSans', size=24)
        page.drawString(200, 800, 'Список ингредиентов')
        page.setFont('OpenSans', size=16)
        height = 750
        for i, (name, data) in enumerate(ingredients_list.items(), 1):
            page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response
        #print(ingredients_list.keys())
        #print(type(ingredients_list.values()))
        #for item in ingredients_list:
        #    print(f'{item} ({ingredients_list[item]["measurement_unit"]}) - {ingredients_list[item]["amount"]}')
        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = ('attachment; '
        #                                   'filename="shopping_list.pdf"')

        #return response
        #self.generate_pdf(ingredients_list)
        #return Response(ingredients_list, status=status.HTTP_200_OK)

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
