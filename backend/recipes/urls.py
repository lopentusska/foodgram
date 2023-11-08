from django.urls import path
from rest_framework import routers

from .views import RecipeViewSet


router = routers.SimpleRouter()
router.register('', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'donwload_shopping_cart/',
        RecipeViewSet.as_view({'get': 'download_shopping_cart'}),
        name='download_shopping_cart'
    ),
]

urlpatterns += router.urls
