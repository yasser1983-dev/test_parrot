from rest_framework import viewsets, permissions

from .dish_factory import DishFactory
from .dishes_service import DishesService
from .serializers import DishSerializer


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        factory = DishFactory()
        self.dish_service = DishesService(factory.get_dish_model())
        self.queryset = self.dish_service.get_all_dish()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.dish_service.get_none_dish()
        return self.dish_service.get_all_dish()
