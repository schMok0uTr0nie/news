from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt

from django.conf import settings

from .models import CustomUser


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)

        auth_data = auth_header.decode('utf-8')

        auth_token = auth_data.split(" ")


        if len(auth_token) != 2:   # if
            raise exceptions.AuthenticationFailed('Token not valid')

        token = auth_token[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")

            username = payload['username']

            user = CustomUser.objects.get(username=username)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is expired, login again')

        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is invalid')

        except CustomUser.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'User does not exist')

        # super().authenticate(request)   # Not needed[!]
        return (user, token)

