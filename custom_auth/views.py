from django.contrib.auth import authenticate, login
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import *
from rest_framework import status, permissions


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        login(request, user)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': "Invalid credentials, try again!"}, status=status.HTTP_401_UNAUTHORIZED)
