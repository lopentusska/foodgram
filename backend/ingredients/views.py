from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.response import Response

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """Viewset for the Ingredient serializer"""
    http_method_names = ('get',)
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True).data

        return Response(serialized_data)

    def get_object(self):
        obj = get_object_or_404(Ingredient, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj
