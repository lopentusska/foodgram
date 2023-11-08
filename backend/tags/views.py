from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for tags."""
    http_method_names = ('get',)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True).data

        return Response(serialized_data)

    def get_object(self):
        obj = get_object_or_404(Tag, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj
