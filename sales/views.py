from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import OrderFilter
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for creating and listing orders."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter


    def get_queryset(self):
        """Filter orders by logged-in waiter."""
        if not self.request.user.is_authenticated:
            return Order.objects.none()
        return self.queryset.all()

    @action(detail=False, methods=['get'])
    def daily_report(self, request):
        """Custom action to retrieve today's orders."""
        from django.utils.timezone import now
        today = now().date()
        orders = self.get_queryset().filter(created_at__date=today)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
