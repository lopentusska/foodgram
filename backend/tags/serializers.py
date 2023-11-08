from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for custom tag."""
    def to_internal_value(self, data):
        return data

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color',)
