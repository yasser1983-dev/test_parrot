from django.urls import path
from reports.views import DailySalesReportView

urlpatterns = [
    path('', DailySalesReportView.as_view(), name='daily_sales_report'),
]
