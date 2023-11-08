from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from recipes.paginations import CustomPagination
from users.models import User
from .serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """Viewset for Follow serializer."""
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return user.following.all()

    def perform_create(self, serializer):
        user = self.request.user
        id = self.kwargs['public_id']
        following = get_object_or_404(User, id=id)

        serializer.save(user=user, following=following)

    def get_object(self):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        id = self.kwargs['public_id']
        following = get_object_or_404(User, id=id)

        try:
            obj = queryset.get(user=user, following=following)
        except ObjectDoesNotExist:
            raise ValidationError('You are not subscribed.')

        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
