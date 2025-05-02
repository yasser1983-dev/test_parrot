import pytest
from unittest.mock import Mock, patch
from sales.serializers import OrderSerializer
from sales.models import Order, Dish


@pytest.mark.django_db
def test_order_serializer_creates_order_successfully():
    # Arrange
    dish1 = Dish.objects.create(name="Pizza", price=10.0)
    dish2 = Dish.objects.create(name="Pasta", price=8.0)

    waiter_user = Mock()
    waiter_user.id = 1

    request = Mock()
    request.user = waiter_user

    factory_mock = Mock()
    order_mock = Mock(spec=Order)
    order_mock.id = 123
    factory_mock.create_order.return_value = order_mock

    items_data = [
        {'dish': dish1.id, 'quantity': 2},
        {'dish': dish2.id, 'quantity': 1}
    ]

    input_data = {
        'customer_name': 'Juan Pérez',
        'items': items_data
    }

    with patch('sales.serializers.log_order_creation.delay') as mock_log_task:
        serializer = OrderSerializer(data=input_data, context={
            'request': request,
            'order_factory': factory_mock
        })

        # Act
        assert serializer.is_valid(), serializer.errors
        order = serializer.save()

        # Assert
        factory_mock.create_order.assert_called_once()

        # Extrae argumentos usados en la llamada al factory
        called_args, called_kwargs = factory_mock.create_order.call_args

        assert called_args[0] == waiter_user
        assert called_args[2] == {'customer_name': 'Juan Pérez'}

        items_passed = called_args[1]
        assert len(items_passed) == 2
        assert items_passed[0]['dish'].id == dish1.id
        assert items_passed[0]['quantity'] == 2
        assert items_passed[1]['dish'].id == dish2.id
        assert items_passed[1]['quantity'] == 1

        mock_log_task.assert_called_once_with(order_mock.id)
        assert order == order_mock

@pytest.mark.django_db
def test_order_serializer_raises_error_without_factory():
    data = {
        'customer_name': 'Juan',
        'items': []
    }
    waiter_user = Mock()
    waiter_user.id = 1

    request = Mock()
    request.user = waiter_user
    context = {'request': request}
    serializer = OrderSerializer(data=data, context=context)
    with pytest.raises(ValueError, match="OrderFactory no fue inyectada en el contexto del serializer"):
        serializer.is_valid(raise_exception=True)
        serializer.save()
