from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json

from .models import TemporaryRegisteredUsers


@csrf_exempt
@api_view(['POST'])
def create_account(request):
    email = json.loads(request.body.decode('utf-8'))["email"]
    subject = 'Welcome to Medicannsales'
    temporary_user = TemporaryRegisteredUsers.objects.create(email=email)
    temporary_user.save()
    html_response = render_to_string('authentication/account_create_email.html',
                                     {'id': temporary_user.id, 'token': temporary_user.id})
    response = {
        'msg': 'Your account has been created successfully, Please activate it '
               'by clicking on the link sent to your email',
        'erc': 1
    }
    send_mail(subject, message="", from_email="georgeclinton105@gmail.com", recipient_list=[email], html_message=html_response)
    return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def account_setup(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data["username"]
    password = data["password"]
    token = data['token']
    temp_account = TemporaryRegisteredUsers.objects.get(id=token)
    response = {
        'msg': '',
        'erc': 0
    }

    if temp_account:
        user = User.objects.create_user(
            username=username,
            email=temp_account.email,
            password=password
        )
        try:
            user.save()
            temp_account.delete()
            response['msg'] = 'Your account has been activated'
            response['erc'] = 1
        except Exception as e:
            print('exception is ', e)

    return JsonResponse(response)
