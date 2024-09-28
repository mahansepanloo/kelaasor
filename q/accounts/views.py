from datetime import datetime,timedelta
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .serializer import *
from random import randint
from .utls import *
from rest_framework.response import Response
from rest_framework import status


class Register(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            code = randint(1000, 9999)
            print(code)
            request.session['register'] = {
                'username': serializer.validated_data['username'],
                'password': serializer.validated_data['password'],
                'phone_number': serializer.validated_data['phone_number'],
                "code":code
            }
            # send_otp_code(serializer.validated_data['phone_number'], code)
#           cache.set(serializer.validated_data['phone_number'], timeout=180)


            return Response('opt code send',status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class OptCode(APIView):
    def post(self,request):
        serializer = OptCodes(data=request.data)
        if serializer.is_valid():
            # if (request.session['code'] == serializer.validated_data['code'] and
            #         datetime.now() <= request.session['register']['time'] + timedelta(seconds=180)):
            if (request.session['register']['code'] == serializer.validated_data['code']):
                User.objects.create_user(username=request.session['register']['username'],
                                         password=request.session['register']['password'],
                                         phone_number=request.session['register']['phone_number'])
                del request.session['register']
                return Response("user created", status=status.HTTP_200_OK)
            return Response("code not corects", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    pass
class RefreshView(TokenRefreshView):
    pass


class Change_password(APIView):
    def post(self,request):
        serializer = ChangeSerializer(data=request.data)
        if serializer.is_valid():
            code = randint(1000, 9999)
            print(code)
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
            request.session['change_password'] = {
                'user': user.username,
                "code":code,
            }
            # send_otp_code(serializer.validated_data['phone_number'], code)
            return Response('ok',status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Change_password2(APIView):
    def put(self,request):
        serializer = ChangeSerializer2(data=request.data)
        if serializer.is_valid():
            # if (request.session['change_password']['code'] == serializer.validated_data['code'] and
            #         datetime.now() <= request.session['change_password']['time'] + timedelta(seconds=180)):
            if (request.session['change_password']['code'] == serializer.validated_data['code']):
                user = User.objects.get(username=request.session['change_password']['user'])
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response('change password',status=status.HTTP_200_OK)
            return Response('code error',status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





