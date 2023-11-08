from rest_framework import serializers

from .models import Ingredient, IngredientQuantity


MIN_INGREDIENT_AMOUNT = 1
MAX_INGREDIENT_AMOUNT = 32000


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Serializer for QuantityIngredient."""
    ingredient = IngredientSerializer(read_only=True)
    amount = serializers.IntegerField(
        min_value=MIN_INGREDIENT_AMOUNT,
        max_value=MAX_INGREDIENT_AMOUNT,
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredient_rep = representation.pop('ingredient')
        for key in ingredient_rep:
            representation[key] = ingredient_rep[key]
        return representation

    class Meta:
        model = IngredientQuantity
        fields = ('ingredient', 'amount',)
