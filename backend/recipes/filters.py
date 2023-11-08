from django_filters.widgets import CSVWidget
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe


class TagFilter(FilterSet):
    tags = filters.BaseCSVFilter(
        distinct=True,
        widget=CSVWidget(),
        method='filter_tags'
    )
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

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__slug__in=value)

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
