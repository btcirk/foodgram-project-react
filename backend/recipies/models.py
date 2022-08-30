from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=200, unique=True)
    color = models.CharField(
        verbose_name='Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField(
        verbose_name='Уникальный слаг', max_length=200, unique=True)

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
    def __str__(self):
        return self.name
