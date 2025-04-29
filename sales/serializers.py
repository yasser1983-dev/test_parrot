from rest_framework import serializers
from .models import Dish, Order, OrderItem

class DishSerializer(serializers.ModelSerializer):
    """Serializer for Dish model."""
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    dish = DishSerializer()  # Serialize the dish

    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    items = OrderItemSerializer(many=True)  # Serialize multiple items for an order

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'total_price', 'waiter', 'created_at', 'items']

    def create(self, validated_data):
        """Override to handle creation of Order and OrderItems."""
        items_data = validated_data.pop('items')  # Extract items data from validated_data
        order = Order.objects.create(**validated_data)  # Create the order

        # Create OrderItems and associate them with the created order
        for item_data in items_data:
            dish_data = item_data.pop('dish')
            dish = Dish.objects.get(id=dish_data['id'])  # Retrieve the dish object
            OrderItem.objects.create(order=order, dish=dish, **item_data)  # Create OrderItem

        # Calculate the total price of the order
        total_price = sum(item_data['quantity'] * dish.price for item_data in items_data)
        order.total_price = total_price
        order.save()  # Save the total price on the order

        return order
