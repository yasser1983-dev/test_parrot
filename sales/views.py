from .services.sales_service import SalesService
from rest_framework import viewsets, permissions
from .factories.order_factory import OrderFactory

from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for creating and listing orders."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        factory = OrderFactory()
        self.sales_service = SalesService(factory.get_order_model(), factory.get_order_item_model())
        self.queryset = self.sales_service.get_all_order()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['order_factory'] = OrderFactory()
        return context

    def get_queryset(self):
        """Filter orders by logged-in waiter."""
        if not self.request.user.is_authenticated:
            return self.sales_service.get_none_order()
        return self.sales_service.get_all_order()
