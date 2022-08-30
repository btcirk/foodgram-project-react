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

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=200,
                            blank=False)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False
    )

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
    ingredient = models.ManyToManyField(Food,
                                        through='Ingredient')

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='which_recipe')
    ingredient = models.ForeignKey(Food,
                                   on_delete=models.PROTECT,
                                   verbose_name='Ингредиент',
                                   related_name='which_ingredient'
                                   )
    amount = models.DecimalField(verbose_name='Количество',
                                 max_digits=4,
                                 decimal_places=0,
                                 blank=False)



