from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_base64.fields import Base64ImageField

from ingredients.models import Ingredient, IngredientQuantity
from ingredients.serializers import IngredientQuantitySerializer
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer

from .models import Recipe


MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 32000


class RecipeMixin:
    def get_is_favorited(self, instance):
        request = self.context.get('request', None)

        if request is None or request.user.is_anonymous:
            return False

        return instance in request.user.favorite_recipes.all()

    def get_is_in_shopping_cart(self, instance):
        request = self.context.get('request', None)

        if request is None or request.user.is_anonymous:
            return False

        return request.user.added_in_shopping_cart(instance)


class GetRecipeSerializer(
    RecipeMixin,
    serializers.ModelSerializer
):
    """Serializer for Recipe model including custom methods."""
    author = UserSerializer()
    ingredients = IngredientQuantitySerializer(
        many=True,
        source='ingredient_amount',
    )
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'cooking_time',
        )


class WriteRecipeSerializer(
    RecipeMixin,
    serializers.ModelSerializer
):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(
        many=True,
    )
    ingredients = IngredientQuantitySerializer(
        many=True,
        source='ingredient_amount',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    name = serializers.CharField(max_length=200)
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError(
                'Choose at least 1 tag.'
            )

        if len(tags) != len(set(tags)):
            raise ValidationError('Can not have same tags.')

        for tag in tags:
            try:
                tag = Tag.objects.get(id=tag)
            except ObjectDoesNotExist:
                raise ValidationError(f'Tag {tag} does not exist.')

        return tags

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise ValidationError(
                'Choose at least 1 ingredient.'
            )

        ingredients_data = set()
        initial_ingredients = self.initial_data['ingredients']

        for ingredient_data in initial_ingredients:
            ingredient_id = ingredient_data['id']

            if ingredient_id in ingredients_data:
                raise ValidationError(
                    f'You have already added ingredient {ingredient_id}'
                )
            ingredients_data.add(ingredient_id)

            try:
                Ingredient.objects.get(id=ingredient_id)
            except ObjectDoesNotExist:
                raise ValidationError(
                    f'Ingredient {ingredient_id} does not exist.'
                )

        return ingredients

    def add_ingredients(self, recipe):
        ingredients_initial_data = self.initial_data['ingredients']
        IngredientQuantity.objects.bulk_create([
            IngredientQuantity(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients_initial_data
        ])
        return recipe

    def add_tags(self, recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        tags = validated_data.pop('tags')
        validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        recipe = self.add_ingredients(recipe)
        recipe.image.save(image_data.name, image_data)
        return self.add_tags(recipe, tags=tags)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.get('ingredient_amount')
        tags = validated_data.get('tags')
        self.validate_ingredients(ingredients)
        self.validate_tags(tags)
        instance = self.add_ingredients(instance)
        instance = self.add_tags(instance, tags=tags)
        instance.save()
        return instance
