import django_rq

from .models import Order


@django_rq.job
def log_order_creation(order_id):
    """Background task to log the creation of a new order."""
    try:
        order = Order.objects.get(id=order_id)
        print(f"Orden creada: {order.customer_name} con precio total {order.total_price} x mesero {order.waiter.email}")
    except Order.DoesNotExist:
        print("Order not found")
