from django.contrib import admin

from ingredients.admin import IngredientQuantityInline
from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_in_favorite', 'get_tags']
    list_filter = ('name', 'author', 'tags')
    inlines = (IngredientQuantityInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def get_tags(self, obj):
        return ', '.join(o.name for o in obj.tags.all())

    def get_in_favorite(self, obj):
        return obj.favorited_by.count()


admin.site.register(Recipe, RecipeAdmin)
