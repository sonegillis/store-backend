from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.response import Response

# Create your views here.
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from .models import TemporaryRegisteredUsers, UserProfile
from .serializers import UserProfileSerializer, UserSerializer
import environ

env = environ.Env()
environ.Env.read_env()


@csrf_exempt
@api_view(['POST'])
def create_account(request):
    email = json.loads(request.body.decode('utf-8'))["email"]
    if User.objects.filter(email=email).exists():
        return JsonResponse({'msg': 'User account already exist with this mail', 'erc': 0})

    subject = 'Welcome to DC Gas Overflow'
    temporary_user, created = TemporaryRegisteredUsers.objects.get_or_create(email=email)
    temporary_user.save()
    html_response = render_to_string('authentication/account_create_email.html',
                                     {'id': temporary_user.id, 'token': temporary_user.id,
                                      'domain': settings.HOST_DOMAIN, 'request': request})

    response = {
        'msg': 'Your account has been created successfully, Please activate it '
               'by clicking on the link sent to your email',
        'erc': 1
    }
    send_mail(subject, message="", from_email="georgeclinton105@gmail.com",
              recipient_list=[email], html_message=html_response)
    return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def account_setup(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data["username"]
    password = data["password"]
    referral = data["referral"]

    token = data['token']
    temp_account = TemporaryRegisteredUsers.objects.get(id=token)
    user_who_referred = UserProfile.objects.filter(referral_code__iexact=referral)

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
            user_profile = UserProfile(user=user, points=0)
            user_profile.save()
            temp_account.delete()

            if user_who_referred.exists():
                user_who_referred[0].points += 10
                user_who_referred[0].save()

            response['msg'] = 'Your account has been activated'
            response['erc'] = 1
        except Exception as e:
            print('exception is ', e)

    return JsonResponse(response)


class UserView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

    def get_serializer(self, *args, **kwargs):
        return UserSerializer(self.get_queryset())


class UserProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args):
        user_profile = UserProfile.objects.get(user_id=self.request.user.id)
        user_profile_serializer = UserProfileSerializer(user_profile, context={'request': self.request})
        return Response(user_profile_serializer.data)

    def post(self, *args):
        state = self.request.data.get('state')
        city = self.request.data.get('city')
        user_address = self.request.data.get('user_address', '')
        phone_number = self.request.data.get('phone_number', '')
        user_profile = UserProfile.objects.get(user_id=self.request.user.id)
        user_profile.state = state
        user_profile.city = city
        user_profile.shipping_address = user_address
        user_profile.phone_number = phone_number
        user_profile.save()
        return JsonResponse({'msg': 'Successfully updated your profile'})
