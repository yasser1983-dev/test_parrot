import django_rq

from .models import Order


@django_rq.job
def log_order_creation(order_id):
    """Background task to log the creation of a new order."""
    try:
        order = Order.objects.get(id=order_id)
        print(f"Order created: {order.customer_name} ordered {order.quantity}x {order.item_name}")
    except Order.DoesNotExist:
        print("Order not found")
