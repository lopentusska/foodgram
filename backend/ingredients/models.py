from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


MIN_INGREDIENT_AMOUNT = 1
MAX_INGREDIENT_AMOUNT = 32000


class Ingredient(models.Model):
    """Ingredient model."""
    name = models.TextField(verbose_name='Имя')
    measurement_unit = models.TextField(verbose_name='Единица')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = '"ingredient"'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_pair',
            )
        ]
        ordering = ['name']


class IngredientQuantity(models.Model):
    """IngredientQuantity model for the amount of the specific ingredient."""
    recipe = models.ForeignKey(
        'recipes_label.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_amount',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_amount',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_INGREDIENT_AMOUNT),
            MaxValueValidator(MAX_INGREDIENT_AMOUNT)
        ),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} {self.amount}'
