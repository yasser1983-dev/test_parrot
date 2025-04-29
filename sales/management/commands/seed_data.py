from django.core.management.base import BaseCommand
from faker import Faker
import random
from sales.models import Dish, Order, OrderItem
from django.contrib.auth import get_user_model
from user.models import User

class Command(BaseCommand):
    help = 'Seed the database with fake dishes and waiters'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake dishes
        for _ in range(20):
            Dish.objects.create(
                name=fake.unique.word().capitalize(),
                price=round(random.uniform(5.0, 30.0), 2)
            )
        self.stdout.write(self.style.SUCCESS('✅ 20 platos creados.'))

        # Create waiter users
        for _ in range(5):
            User.objects.create_user(
                email=fake.unique.email(),
            )
        self.stdout.write(self.style.SUCCESS('5 meseros creados.'))

        self.stdout.write(self.style.SUCCESS('Datos de prueba generados con éxito.'))
