from rest_framework.authtoken.models import Token
from sales.models import OrderItem, Order
from user.models import User


class OrderFactory:

    def create_order(self, waiter, items_data, extra_order_data=None):
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
