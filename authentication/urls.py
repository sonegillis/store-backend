from django.urls import path

from .views import create_account, account_setup

urlpatterns = [
    path('create-account', create_account),
    path('account-setup', account_setup)
]
