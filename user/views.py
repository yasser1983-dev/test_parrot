from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from rest_framework.authtoken.models import Token  # O usa JWT si prefieres

class EmailOnlyAuthView(APIView):
    """Email-only authentication (no password)"""

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Se requiere un correo electrónico'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            if not user.is_active:
                return Response({'error': 'Usuario inactivo'}, status=status.HTTP_403_FORBIDDEN)

            # Create a token if it doesn't exist
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Correo no registrado'}, status=status.HTTP_404_NOT_FOUND)
