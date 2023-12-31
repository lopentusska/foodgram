from rest_framework import routers

from .views import UserViewSet


router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = router.urls
