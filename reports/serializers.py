from rest_framework import serializers


class DailySalesReportSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
