from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.serializers import GetRecipeSerializer
from users.models import User

from .models import Follow

RECIPES_SINGLE_PAGE_LIMIT = 3
PAGE_NUMBER = 1


class FollowingSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
            'is_subscribed',
        ]

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = (
            request.query_params.get('recipes_limit')
            or RECIPES_SINGLE_PAGE_LIMIT
        )
        recipes = obj.recipe_set.all()
        paginator = Paginator(recipes, limit)
        page = request.query_params.get('page') or PAGE_NUMBER
        try:
            recipes_paginated = paginator.page(page)
        except EmptyPage:
            recipes_paginated = paginator.page(paginator.num_pages)

        serializer = GetRecipeSerializer(
            recipes_paginated,
            many=True,
            context={'request': request}
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe_set.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.followers.filter(user=user).exists()


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow model."""
    following = FollowingSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('following',)
        read_only_fields = ('following',)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        following_id = self.context['view'].kwargs.get('public_id')
        following = get_object_or_404(User, id=following_id)

        if request.method == 'POST':
            if following.followers.filter(user=user).exists():
                raise ValidationError('Can not subscribe twice.')
            if user == following:
                raise ValidationError('Can not subscribe on yourself.')

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return data['following']
