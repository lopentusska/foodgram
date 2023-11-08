from django.urls import re_path
from rest_framework import routers

from .views import FollowViewSet

router = routers.SimpleRouter()
router.register('subscriptions', FollowViewSet, basename='follows')


urlpatterns = [
    re_path(
        r'(?P<public_id>[0-9a-f-]+)/subscribe/',
        FollowViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='follow'
    ),
]

urlpatterns += router.urls
