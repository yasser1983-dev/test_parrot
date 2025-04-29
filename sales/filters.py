import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    """Filter for searching orders by date range."""
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['start_date', 'end_date']
