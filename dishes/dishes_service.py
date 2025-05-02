from .models import Dish


class DishesService:
    def __init__(self, dish_model: Dish):
        self.Dish = dish_model

    def get_all_dish(self):
        return self.Dish.objects.all()

    def get_none_dish(self):
        return self.Dish.objects.none()
