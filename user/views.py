from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sales.order_factory import OrderFactory

from .user_service import UserService


class EmailOnlyAuthView(APIView):
    """Email-only authentication (no password)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        factory = OrderFactory()
        self.user_service = UserService(factory.get_user_model(), factory.get_user_model(), factory.get_token_model())

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Se requiere un correo electrónico'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.user_service.get_user_by_email(email)
        token = self.user_service.get_token(user)
        if token is None:
            return Response({'error': 'Usuario inactivo'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'token': token.key}, status=status.HTTP_200_OK)
