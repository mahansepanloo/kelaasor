from datetime import datetime,timedelta
from classs.models import Classs
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .serializer import *
from random import randint
from .utls import *
from rest_framework.response import Response
from rest_framework import status
from exercise.models import *



class Register(APIView):
    """
    Handles user registration by validating input data and sending an OTP code.

    Args:
        request: The request object containing user data (username, password, phone number).

    Returns:
        Response: Returns a success message with status 200, or validation errors with status 400.
    """
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
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OptCode(APIView):
    """
    Validates the provided OTP code and creates a new user if valid.

    Args:
        request: The request object containing the OTP code.

    Returns:
        Response: Returns a success message if user is created or an error message with status 400.
    """
    def post(self,request):
        if not request.session.get('register'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
    """
    Processes password change requests by validating user phone number and sending a verification code.

    Args:
        request: The request object containing the phone number.

    Returns:
        Response: Returns a success message with status 200, or validation errors with status 400.
    """
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



class EditUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        """
        Retrieves the user profile and related items.

        Args:
            request: The request object.

        Returns:
            Response: Returns user data along with related items or error if the user does not exist.
        """
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response('user does not exist', status=status.HTTP_400_BAD_REQUEST)
        items = Classs.objects.filter(user=user)
        serializer = EditProfileSerializer(instance=user, partial=True)
        serializer_data = serializer.data
        serializer_data['items'] = []
        for item in items:
            serializer_data['items'].append({'name': item.name,
                                             "id":item.id})
        return Response(serializer_data,status=status.HTTP_200_OK)

    def put(self, request):
        """
        Updates the user profile with the provided data.

        Args:
            request: The request object containing the updated user data.

        Returns:
            Response: Returns updated user data or validation errors with status 400.
        """
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EditProfileSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Removes the user from a specified class.

        Args:
            request: The request object containing the identifier of the class to be removed from.

        Returns:
            Response: Returns a success message if user is removed or error messages with status 400.
        """
        data = Deleteclass(data=request.data)
        if data.is_valid():
            try:
                item = Classs.objects.get(id=data.validated_data['id_class'])
            except Classs.DoesNotExist:
                return Response("Class does not exist", status=status.HTTP_400_BAD_REQUEST)
            if request.user in item.user.all():
                item.user.remove(request.user)
                return Response("User removed", status=status.HTTP_200_OK)
            else:
                return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)




class UserSocer(APIView):
    """
    Retrieves exercises related to the user in a specified class.

    Args:
        request: The request object.
        class_id: The ID of the class to retrieve exercises for.

    Returns:
        Response: Returns exercise data or error if exercises or class are not found.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, class_id):
        try:
            socers = Socer.objects.filter(classs_id=class_id, user=request.user)
            s = ExerciseSerializer(instance=socers, many=True)
            rezsocer = RezScore.objects.filter(user=request.user, sub__exercise__classs_id=class_id)
            ss = ExerciseSerializer4(instance=rezsocer,many=True)
        except ExerciseModel.DoesNotExist:
            return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=(s.data,ss.data))