from django.db import models


class Dish(models.Model):
    """Model to store individual dish."""
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"
