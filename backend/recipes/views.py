from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredients.models import IngredientQuantity
from users.permissions import UserPermission
from .filters import TagFilter
from .models import Recipe
from .paginations import CustomPagination
from .serializers import GetRecipeSerializer, WriteRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe views including custom method for adding
    recipes in favorites, shopping cart.
    """
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (UserPermission,)
    queryset = Recipe.objects.all().distinct()
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend,)
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('created',)
    ordering = ('-created',)
    filter_class = TagFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetRecipeSerializer
        return WriteRecipeSerializer

    def get_object(self):
        obj = get_object_or_404(Recipe, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        user = self.request.user

        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=self.kwargs['pk'])
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if user.in_favorite(recipe):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.favorite(recipe)

            data = {
                'id': recipe.id,
                'name': recipe.name,
                'image': recipe.image.url,
                'cooking_time': recipe.cooking_time,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])

            if not user.in_favorite(recipe):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.remove_favorite(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        recipes_in_cart = Recipe.objects.filter(
            in_shopping_cart=self.request.user
        )
        ingredient_amounts = defaultdict(float)

        for recipe in recipes_in_cart:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                obj_quantity = IngredientQuantity.objects.get(
                    recipe=recipe,
                    ingredient_id=ingredient.id,
                    ingredient=ingredient,
                )
                ingredient_name = ingredient.name
                ingredient_measurement_unit = ingredient.measurement_unit
                ingredient_amounts[(
                    ingredient_name,
                    ingredient_measurement_unit
                )] += obj_quantity.amount

        shopping_cart_ingredients = []
        for (ingredient, measurement_unit), amount in (
                ingredient_amounts.items()
        ):
            shopping_cart_ingredients.append(
                f'{ingredient} ({measurement_unit}) - {amount}'
            )

        text_content = '\n'.join(shopping_cart_ingredients)

        return Response(
            text_content,
            content_type='text/plain',
            status=status.HTTP_200_OK
        )

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        user = self.request.user

        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=self.kwargs['pk'])
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if user.added_in_shopping_cart(recipe):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.add_shopping_cart(recipe)

            data = {
                'id': recipe.id,
                'name': recipe.name,
                'image': recipe.image.url,
                'cooking_time': recipe.cooking_time,
            }

            return Response(data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
            if not user.added_in_shopping_cart(recipe):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.remove_shopping_cart(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
