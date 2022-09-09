from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientsInstanceInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ["name"]


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "favorites_count")
    list_filter = ("author", "name", "tags")
    inlines = [IngredientsInstanceInline]

    def favorites_count(self, obj):
        return obj.favorites.count()

    favorites_count.short_description = "Добавлений в избранное"
