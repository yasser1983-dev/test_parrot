import random

from dishes.models import Dish
from django.core.management.base import BaseCommand
from faker import Faker
from sales.models import Order, OrderItem
from user.models import User

ingredientes = ["Pollo", "Res", "Cerdo", "Pescado", "Camarones", "Tofu", "Frijoles", "Lentejas", "Arroz", "Pasta",
                "Papas", "Ensalada", "Verduras Mixtas", "Hongos"]
preparaciones = ["a la Parrilla", "Al Horno", "Empanizado", "Salteado", "En Salsa", "Estofado", "Frito", "Relleno"]
adjetivos = ["Delicioso", "Exquisito", "Sabroso", "Casero", "Especial", "Tradicional", "Picante", "Suave", "Crujiente"]
complementos = ["con Limón", "con Cilantro", "con Queso", "con Crema", "con Aguacate", "con Tocino", "con Champiñones"]


def generate_dish_name():
    partes = []
    # Asegurar que al menos un ingrediente o preparación se elija
    if random.random() < 0.5:
        partes.append(random.choice(ingredientes))
    else:
        partes.append(random.choice(preparaciones))

    if random.random() < 0.4:
        partes.insert(0, random.choice(adjetivos))
    if random.random() < 0.5:
        partes.append(random.choice(complementos))

    return " ".join(partes).capitalize()


class Command(BaseCommand):
    help = 'Seed the database with fake dishes and waiters'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake dishes
        for _ in range(20):
            Dish.objects.create(
                name=generate_dish_name(),
                price=round(random.uniform(5.0, 30.0), 2)
            )
        self.stdout.write(self.style.SUCCESS('20 platillos creados.'))

        # Create waiter users
        for _ in range(5):
            User.objects.create_user(
                email=fake.unique.email(),
            )
        self.stdout.write(self.style.SUCCESS('5 meseros creados.'))

        self.stdout.write(self.style.SUCCESS('Datos de prueba generados con éxito.'))
