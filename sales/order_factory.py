from rest_framework.authtoken.models import Token
from sales.models import OrderItem, Order
from user.models import User


class OrderFactory:

    def create_order(self, waiter, items_data, extra_order_data=None) -> Order:
        """
        Creates a new Order instance along with its associated OrderItems.

        Args:
            waiter (User): The user (waiter) responsible for the order.
            items_data (list): A list of dictionaries containing 'dish' and 'quantity' keys.
                               Example: [{'dish': dish_instance, 'quantity': 2}, ...]
            extra_order_data (dict, optional): Additional fields to be included in the Order creation.

        Returns:
            Order: The created Order object with its related OrderItems.

        Note:
            Only items with a quantity greater than 0 are processed and included.
            The total price is calculated based on the price and quantity of valid dishes.
        """
        total_price = 0
        valid_items = []
        if extra_order_data is None:
            extra_order_data = {}

        for item in items_data:
            if item['quantity'] > 0:
                total_price += item['quantity'] * item['dish'].price
                valid_items.append(item)

        order = Order.objects.create(
            waiter=waiter,
            total_price=total_price,
            **extra_order_data
        )

        for item in valid_items:
            OrderItem.objects.create(
                order=order,
                dish=item['dish'],
                quantity=item['quantity']
            )

        return order

    def get_user_model(self):
        return User

    def get_order_model(self):
        return Order

    def get_order_item_model(self):
        return OrderItem

    def get_token_model(self):
        return Token
