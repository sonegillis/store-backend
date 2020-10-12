from django.urls import path

from .views import create_account, account_setup, UserProfileView

urlpatterns = [
    path('create-account', create_account),
    path('account-setup', account_setup),
    path('update-profile', UserProfileView.as_view()),
    path('user-profile', UserProfileView.as_view())
]
