from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'color', 'slug')
        model = Tag
