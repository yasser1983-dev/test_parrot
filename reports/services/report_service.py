from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce

from sales.models import OrderItem


class DailySalesReportService:

    def get_grouped_report(self, queryset, start_date, end_date):
        return (
            queryset
            .filter(order__created_at__range=(start_date, end_date))
            .values(name=F('dish__name'))
            .annotate(
                total_quantity=Sum('quantity'),
                total_price=Sum(F('quantity') * F('dish__price'))
            )
            .order_by('-total_quantity')
        )
