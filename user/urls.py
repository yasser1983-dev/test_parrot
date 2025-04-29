from django.urls import path
from .views import EmailOnlyAuthView

urlpatterns = [
    path('auth/email-login/', EmailOnlyAuthView.as_view(), name='email-login'),
]
