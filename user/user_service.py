from rest_framework.authtoken.models import Token
from sales.models import Order
from user.models import User


class UserService:
    def __init__(self, user_model: User, order_model: Order, token_model: Token):
        self.User = user_model
        self.Order = order_model
        self.Token = token_model

    def get_user_by_email(self, email: str):
        try:
            return self.User.objects.get(email=email)
        except self.User.DoesNotExist:
            return None

    def get_none_data_order(self):
        return self.Order.objects.none()

    def get_token(self, user):
        try:
            if not user or not user.is_active:
                return None

            token, created = self.Token.objects.get_or_create(user=user)
            return token
        except self.User.DoesNotExist:
            return None
