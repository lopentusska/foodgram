from django_filters.rest_framework import FilterSet, filters
from django_filters.fields import MultipleChoiceField

from recipes.models import Recipe


class TagsFilter(filters.AllValuesMultipleFilter):
    field_class = MultipleChoiceField


class TagFilter(FilterSet):
    tags = TagsFilter(field_name='tags__slug')
    author = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorited_by=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(in_shopping_cart=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        ]
