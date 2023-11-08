from django.contrib import admin

from .models import Ingredient, IngredientQuantity


class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    inlines = (IngredientQuantityInline, )
    list_filter = ('name',)

    class Meta:
        model = Ingredient


admin.site.register(Ingredient,)
