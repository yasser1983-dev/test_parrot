# import json
from unittest.mock import Mock, patch

import pytest
from rest_framework import status
# from rest_framework.request import Request
from rest_framework.test import APIClient
# from rest_framework.test import APIRequestFactory

from .views import EmailOnlyAuthView


# @pytest.mark.django_db
# def test_post_returns_token_if_user_is_active():
#     factory = APIRequestFactory()
#     data = {'email': 'test@example.com'}
#
#     request = factory.post('/api/user/email-login/', data, format='json')
#
#     # Mock del usuario y del token
#     mock_user = Mock()
#     mock_token = Mock()
#     mock_token.key = 'abc123'
#
#     with patch('user.views.EmailOnlyAuthView.user_service') as mock_service:
#         mock_service.get_user_by_email.return_value = mock_user
#         mock_service.get_token.return_value = mock_token
#
#         # Crea una instancia de la vista y ejecuta el request
#         view = EmailOnlyAuthView.as_view()
#         response = view(request)
#
#         # Verificaciones
#         assert response.status_code == 200
#         assert response.data == {'token': 'abc123'}


@pytest.mark.django_db
def test_post_returns_400_if_email_missing():
    client = APIClient()

    with patch('user.views.EmailOnlyAuthView.__init__', return_value=None):
        view = EmailOnlyAuthView()
        view.user_service = Mock()

        # Hacer override del método usando .as_view()
        response = view.as_view()(client.post('/api/user/email-login', {}, format='json').wsgi_request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'error': 'Se requiere un correo electrónico'}



@pytest.mark.django_db
def test_post_returns_403_if_token_is_none():
    client = APIClient()
    mock_user = Mock()

    with patch('user.views.EmailOnlyAuthView.__init__', return_value=None):
        view = EmailOnlyAuthView()
        view.user_service = Mock()
        view.user_service.get_user_by_email.return_value = mock_user
        view.user_service.get_token.return_value = None

        response = view.as_view()(client.post('/api/user/email-login', {'email': 'inactive@example.com'}, format='json').wsgi_request)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {'error': 'Usuario inactivo'}

