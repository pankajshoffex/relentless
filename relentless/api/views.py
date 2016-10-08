from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from api.models import MyUser
from api.CsrfExemptSessionAuthenticationView import CsrfExemptSessionAuthentication, BasicAuthentication


class Login(APIView):
    """
    Login api for IOS user
    user needs to provide 'username' and 'password' for authentication.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = dict()
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
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


class UserList(APIView):
    """
    API - List of all Users
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        data = MyUser.objects.all()
        data_sr = UserSerializer(data, many=True)
        # Ret data
        data = {'errorCode': False, 'result': data_sr.data}
        return Response(data)

    def post(self, request):
        data_sr = UserSerializer(data=request.data)
        if data_sr.is_valid():
            data_sr.save()
            data = {'error': False, 'result': data_sr.data}
            return Response(data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {'error': True, 'result': data_sr.errors}
        return Response(data)


class UserDetail(APIView):
    """
    API : Get/Update/delete the details of the User
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except ObjectDoesNotExist as err:
            raise ObjectDoesNotExist(err)

    def get(self, request, pk):
        data = self.get_object(pk)
        data_sr = UserSerializer(data)
        return Response(data_sr.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        put = QueryDict(request.body)
        data_sr = UserSerializer(user, data=request.data, partial=True)
        if data_sr.is_valid():
            data_sr.save()
            data = {'error': False, 'result': data_sr.data}
            return Response(data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {'error': True, 'result': data_sr.errors}
        return Response(data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        data = {'error': False}
        return Response(data)
