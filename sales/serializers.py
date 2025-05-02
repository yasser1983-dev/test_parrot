from rest_framework import serializers

from .models import Dish, Order, OrderItem
from .tasks import log_order_creation


class DishSerializer(serializers.ModelSerializer):
    """Serializer for Dish model."""

    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # 🔥 Solo lectura

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'total_price', 'waiter', 'created_at', 'items']
        read_only_fields = ['waiter']

    def create(self, validated_data):
        """Override to handle creation of Order and OrderItems."""
        request = self.context['request']
        waiter = request.user
        items_data = validated_data.pop('items')
        extra_data = {**validated_data}

        factory = self.context.get('order_factory')
        if factory is None:
            raise ValueError("OrderFactory no fue inyectada en el contexto del serializer")

        order = factory.create_order(waiter, items_data, extra_data)
        # Calls the asynchronous task to record the creation of the order
        log_order_creation.delay(order.id)

        return order
