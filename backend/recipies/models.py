from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=200, unique=True)
    color = models.CharField(
        verbose_name='Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField(
        verbose_name='Уникальный слаг', max_length=200, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=200,
                            blank=False)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               blank=False)
    title = models.CharField(verbose_name='Название',
                             max_length=200,
                             blank=False)
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='uploads/',
                              blank=False)
    text = models.TextField(verbose_name='Текстовое описание', blank=False)
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name='Тег',
                            related_name='recipe',
                            blank=False)
    time = models.DecimalField(verbose_name='Время готовки',
                               max_digits=3,
                               decimal_places=0,
                               blank=False)
    ingredient = models.ManyToManyField(Ingredient,
                                        through='IngredientAmount')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='which_recipe')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.PROTECT,
                                   verbose_name='Ингредиент',
                                   related_name='which_ingredient'
                                   )
    amount = models.PositiveSmallIntegerField(verbose_name='Количество',
                                              blank=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
    ]

    def __str__(self):
        return self.ingredient


