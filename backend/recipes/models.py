from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag


MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 32000


class Recipe(models.Model):
    """Recipe model."""
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлён',
    )
    author = models.ForeignKey(
        to='users_label.User',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.TextField(verbose_name='Название',)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    text = models.TextField(verbose_name='Описание',)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ingredients_label.IngredientQuantity',
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Таги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_COOKING_TIME),
            MaxValueValidator(MAX_COOKING_TIME)
        ),
        verbose_name='Время приготовления',
    )

    class Meta:
        db_table = '"recipe"'
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'
