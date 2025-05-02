from datetime import datetime, time, timedelta, timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from sales.order_factory import OrderFactory
from sales.sales_service import SalesService

from .filters import OrderFilter
from .serializers import DailySalesReportSerializer
from .services.report_service import DailySalesReportService


class DailySalesReportView(GenericAPIView):
    """View to generate the sales report grouped by item."""

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        factory = OrderFactory()
        self.daily_sales_report_service = DailySalesReportService()
        self.sales_service = SalesService(factory.get_order_model(), factory.get_order_item_model())
        self.queryset = self.sales_service.get_all_order_item()

    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return Response(
                {'error': 'Debe especificar "start_date" y "end_date" en formato YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = datetime.combine(datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date(),
                                      time.min)  # 00:00:00
        end_date = datetime.combine(datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date(),
                                    time.max)  # 23:59:59.999999

        utc_minus_6 = timezone(timedelta(hours=-6))

        start_datetime = datetime.combine(start_date, time.min).replace(tzinfo=utc_minus_6)
        end_datetime = datetime.combine(end_date, time.max).replace(tzinfo=utc_minus_6)

        if not start_date or not end_date:
            return Response(
                {'error': 'Las fechas proporcionadas no son válidas. Por favor use el formato YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.sales_service.get_order_dish()

        report = self.daily_sales_report_service.get_grouped_report(queryset, start_datetime, end_datetime)

        serializer = DailySalesReportSerializer(report, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
