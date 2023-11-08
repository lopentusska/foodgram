from rest_framework import routers

from .views import IngredientViewSet


router = routers.SimpleRouter()
router.register('', IngredientViewSet, basename='ingredients')

urlpatterns = router.urls
