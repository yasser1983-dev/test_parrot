from rest_framework import serializers
from .models import Dish, Order, OrderItem

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

    def create(self, validated_data):
        """Override to handle creation of Order and OrderItems."""
        items_data = validated_data.pop('items')

        order = Order(**validated_data)

        total_price = 0
        for item_data in items_data:
            dish = item_data['dish']
            if item_data['quantity'] > 0:
                total_price += item_data['quantity'] * dish.price

        order.total_price = total_price
        order.save()

        for item_data in items_data:
            dish = item_data['dish']
            OrderItem.objects.create(order=order, dish=dish, quantity=item_data['quantity'])

        return order

