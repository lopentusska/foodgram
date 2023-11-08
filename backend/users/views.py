from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.paginations import CustomPagination
from .models import User
from .permissions import UserPermission
from .serializers import RegisterSerializer, UserSerializer


class UserViewSet(UserViewSet):
    """Viewset for user serializer, with 'me' function."""
    http_method_names = ('get', 'post', 'patch',)
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_object(self):
        obj = get_object_or_404(User, id=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'id': user.id,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(
        [
            'get', 'put', 'patch', 'delete'
        ], detail=False, permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        method = {
            'GET': self.retrieve,
            'PUT': self.update,
            'PATCH': self.partial_update,
            'DELETE': self.destroy
        }

        received_method = request.method
        handler = method.get(received_method)
        return handler(request, *args, **kwargs)
