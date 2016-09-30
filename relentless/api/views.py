from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from api.CsrfExemptSessionAuthenticationView import CsrfExemptSessionAuthentication, BasicAuthentication


class Login(APIView):
    """
    Login api for IOS user
    user needs to provide 'username' and 'password' for authentication.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = dict()
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Correct password, and the user is marked "active"
                login(request, user)
                # Get user details
                user_detail = User.objects.get(pk=user.id)
                user_serializer = UserSerializer(user_detail)
                # ret data
                data['resultCode'] = False
                data['resultMessage'] = user_serializer.data
                return Response(data)
            else:
                data['resultCode'] = True
                data['resultMessage'] = 'This user is not active'
                return Response(data)
        else:
            data['resultCode'] = True
            data['resultMessage'] = 'Invalid username or password'
            return Response(data)


class Logout(APIView):
    def get(self, request):
        data = dict()
        logout(request)
        data['resultCode'] = False
        data['resultMessage'] = "logged out successfully"
        return Response(data)
