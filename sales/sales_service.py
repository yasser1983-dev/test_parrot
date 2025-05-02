from .models import Order, OrderItem


class SalesService:
    def __init__(self, order_model: Order, order_item_model: OrderItem):
        self.Order = order_model
        self.OrderItem = order_item_model

    def get_order_dish(self):
        return self.OrderItem.objects.select_related('dish', 'order')

    def get_all_order_item(self):
        return self.OrderItem.objects.all()

    def get_none_order(self):
        return self.Order.objects.none()

    def get_all_order(self):
        return self.Order.objects.all()
