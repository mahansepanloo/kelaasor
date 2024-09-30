import datetime
from .tasks import send_email_to_customer
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction




class CreateClass(APIView):
    """
get :
        Returns a list of all classes where the user is a teacher.

    post:
        Creates a new class with the provided details.

        Required fields:
            - type: Type of the class (1 for public, 2 for private)
            - is_privet: Boolean indicating if the class is private
            - is_email: Boolean indicating if email notifications are enabled
            - password: Password for the class (if private)
            - name: Name of the class
            - description: Description of the class

        Optional fields:
            - Validation: Validation code for joining a private class
            - stock: Number of available spots in the class (default is infinity if null)
            - start: Start date join the class
            - finish: End date join  the class

    """
    permission_classes = [IsAuthenticated]
    def get(self,request):
        item = Classs.objects.filter(teacher__id=request.user.id)
        serilazers = CreateClassSerializer(instance=item, many=True)
        return Response(serilazers.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = CreateClassSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    item = serializer.save()
                    class_type = request.data.get('type')
                    if class_type == 2:
                        item.is_privet = True
                        item.save()
                    elif class_type == 1:
                        item.type = 'public'
                    else:
                        return Response({"error": "Invalid type."}, status=status.HTTP_400_BAD_REQUEST)
                item.teacher.add(request.user)
                if item.is_privet == True and item.is_email == True:
                    ListUserPrivet.objects.create(classs=item,is_email=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                elif item.is_privet == True and item.is_password == True:
                    ListUserPrivet.objects.create(classs=item,is_password=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                elif item.is_privet == False:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AddPublicClass(APIView):
    """
            get:
        Adds the authenticated user to the public class identified by id_class.

    Parameters:
        - id_class: ID of the class to join.

    Response:
        - If the class is not found, returns a 404 error.
        - If the user is already added, returns a message indicating so.
        - If the class is not available for joining, returns an appropriate error message.
        - If successful, adds the user to the class and reduces the stock.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class)
        except Classs.DoesNotExist:
            return Response('Class not found', status=status.HTTP_404_NOT_FOUND)
        if item.is_privet == False:
            if request.user in item.user.all():
                return Response('already added to class', status=status.HTTP_200_OK)
            now = datetime.date.today()
            if item.start and item.start > now:
                return Response('You cannot add class at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.finish and item.finish < now:
                return Response('You cannot add class at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.stock and item.stock > 0:
                try:
                    with transaction.atomic():
                        item.user.add(request.user)
                        item.stock -= 1
                        item.save()
                        return Response("Added to class", status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            elif not item.stock:
                item.user.add(request.user)
                item.save()
                return Response("Added to class", status=status.HTTP_201_CREATED)
            else:
                return Response('class not stock', status=status.HTTP_400_BAD_REQUEST)
        return Response(" no access ", status=status.HTTP_200_OK)





class AdduserPrivet(APIView):
    """
    API endpoint for adding users to a private class.

    post:
        Adds a list of user IDs to the user_permissions of a private class.

    Parameters:
        - id_class: ID of the private class to which users are being added.

    Request body:
        - user: List of user IDs to add.

    Response:
        - If the class is not found or the user is not authorized, returns an error.
        - If successful, adds the users to the class.
    """
    permission_classes = [IsAuthenticated]
    def post(self,request,id_class):
        try:
            item = Classs.objects.get(teacher=request.user,id=id_class, is_privet=True)
            listuser = ListUserPrivet.objects.get(classs=item)
        except Classs.DoesNotExist:
            return Response("class not find",status=status.HTTP_404_NOT_FOUND)
        serializer = AdduserPrivetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    if listuser.is_email == True:
                        for i in serializer.validated_data['user']:
                            listuser.user.add(i)
                        l = [u.email for u in listuser.user.all()]
                        send_email_to_customer.delay(request=request.data, subject='invite',
                                                     message=f"http://127.0.0.1:8000/class/addprivete/{item.id}/{item.Validation}",
                                                     recipient_list=l)
                        return Response('add',status=status.HTTP_201_CREATED)

                    if listuser.is_password == True:
                        for i in serializer.validated_data['user']:
                            listuser.user.add(i)
                        l = [u.email for u in listuser.user.all()]
                        send_email_to_customer.delay(request=request.data, subject='invite',
                                                 message=f"password == {item.Validation}",
                                                 recipient_list=l)
                        return Response('add', status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class AddPrivatePassword(APIView):
    """

    post:
        Allows a user to join a private class by providing the class ID and password.

    Parameters:
        - id_class: ID of the class to join.

    Request body:
        - password: The password required to join the class.

    Response:
        - If the class is not found, returns a 404 error.
        - If the password is incorrect, returns an error.
        - If the user is already added, returns a message indicating so.
        - If successful, adds the user to the class and reduces the stock.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request,id_class):
        try:
            item = Classs.objects.get(id=id_class, is_privet=True, is_password=True)
            listuser = ListUserPrivet.objects.get(classs=item, is_password=True)
        except (Classs.DoesNotExist, ListUserPrivet.DoesNotExist):
            return Response('Class not found', status=status.HTTP_404_NOT_FOUND)
        serializers = CodserSerializer(data=request.data)
        if serializers.is_valid():
            if item.Validation != serializers.validated_data['password']:
                return Response('password not match', status=status.HTTP_400_BAD_REQUEST)
            if request.user not in listuser.user.all():
                return Response('not access', status=status.HTTP_400_BAD_REQUEST)
            if request.user in item.user.all():
                return Response('already added to class', status=status.HTTP_200_OK)
            now = datetime.date.today()
            if item.start and item.start > now:
                return Response('You cannot add class at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.finish and item.finish < now:
                return Response('You cannot add class at this time', status=status.HTTP_400_BAD_REQUEST)

            if item.stock and item.stock > 0:
                try:
                    with transaction.atomic():
                        item.user.add(request.user)
                        item.stock -= 1
                        item.save()
                        return Response("Added to class", status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            elif not item.stock:
                item.user.add(request.user)
                item.save()
                return Response("Added to class", status=status.HTTP_201_CREATED)
            else:
                return Response('class not stock', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPrivateEmailClass(APIView):
    """
    get id_class and key in link send to email and join class
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,id_class,key):
        try:
            item = Classs.objects.get(id=id_class, is_privet=True, is_email=True)
            listuser = ListUserPrivet.objects.get(classs=item, is_email=True)
        except (Classs.DoesNotExist, ListUserPrivet.DoesNotExist):
            return Response('Class not found', status=status.HTTP_404_NOT_FOUND)
        if item.Validation != key:
            return Response('you not permissons join class', status=status.HTTP_400_BAD_REQUEST)
        if request.user in listuser.user.all():
            if request.user in item.user.all():
                return Response('YOU ARE JOIND CLASS NOW', status=status.HTTP_400_BAD_REQUEST)
            now = datetime.date.today()
            if item.start and item.start > now:
                    return Response('You cannot add class at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.finish and item.finish < now:
                    return Response('You cannot add class at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.stock and item.stock > 0:
                try:
                    with transaction.atomic():
                        item.user.add(request.user)
                        item.stock -= 1
                        item.save()
                        return Response("Added to class", status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            elif not item.stock:
                item.user.add(request.user)
                item.save()
                return Response("Added to class", status=status.HTTP_201_CREATED)
            else:
                return Response('class not stock', status=status.HTTP_400_BAD_REQUEST)

        else :
            return Response('you not permissons join class', status=status.HTTP_400_BAD_REQUEST)


class Edite(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,id_class):
        try:
            item = Classs.objects.get(id=id_class,teacher=request.user)
        except Classs.DoesNotExist:
            return Response('not found class', status=status.HTTP_404_NOT_FOUND)

        s =ShowInfoClass(item)
        return Response(data=s.data , status=status.HTTP_200_OK)

    def put(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class, teacher=request.user)
        except Classs.DoesNotExist:
            return Response('not found class', status=status.HTTP_404_NOT_FOUND)
        serializers = Editeclass(data=request.data)
        if serializers.is_valid():
            if serializers.validated_data.get('teacher'):
                for i in serializers.validated_data['teacher']:
                    item.teacher.add(i)
                    return Response('Added to class', status=status.HTTP_200_OK)
            if serializers.validated_data.get('ta'):
                for i in serializers.validated_data['ta']:
                    item.ta.add(i)
                    return Response(' ta Added to class', status=status.HTTP_200_OK)
            return Response('error', status=status.HTTP_400_BAD_REQUEST)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class, teacher=request.user)
        except Classs.DoesNotExist:
            return Response('not found class', status=status.HTTP_404_NOT_FOUND)
        serializers = Editeclass(data=request.data)
        if serializers.is_valid():
            if serializers.validated_data.get('user'):
                    try:
                        user = User.objects.get(id=int(serializers.validated_data.get('user')))
                    except User.DoesNotExist:
                        return Response('user not founds', status=status.HTTP_404_NOT_FOUND)
                    if user in item.user.all():
                        item.user.remove(user)
                        return Response(f'{user.username}remove to class', status=status.HTTP_200_OK)
                    return Response('user not found', status=status.HTTP_404_NOT_FOUND)
            return Response('error',status=status.HTTP_400_BAD_REQUEST)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)





