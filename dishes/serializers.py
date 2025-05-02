from rest_framework import serializers

from .models import Dish


class DishSerializer(serializers.ModelSerializer):
    """Serializer for Dish model."""

    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']
