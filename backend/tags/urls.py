from rest_framework import routers

from .views import TagViewSet


router = routers.SimpleRouter()
router.register('', TagViewSet, basename='tags')

urlpatterns = router.urls
