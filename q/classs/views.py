import datetime
import random

from .tasks import send_email_to_customer
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .permissions import *
from rest_framework.generics import ListCreateAPIView




class CreateClass(APIView):
    """
get :
        Returns a list of all classes where the user is a teacher.

    post:
        Creates a new classs with the provided details.

        Required fields:
            - type: Type of the classs (1 for public, 2 for private)
            - is_privet: Boolean indicating if the classs is private
            - is_email: Boolean indicating if email notifications are enabled
            - password: Password for the classs (if private)
            - name: Name of the classs
            - description: Description of the classs

        Optional fields:
            - Validation: Validation code for joining a private classs
            - stock: Number of available spots in the classs (default is infinity if null)
            - start: Start date join the classs
            - finish: End date join  the classs

    """
    permission_classes = [IsAuthenticated]
    def get(self,request):
        item = Classs.objects.filter(teacher__id=request.user.id)
        serilazers = CreateClassSerializer(instance=item, many=True)
        return Response(serilazers.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = CreateClassSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['type'] == "1" and (serializer.validated_data['is_email'] == True or
                                                           serializer.validated_data['is_password'] == True):
                return Response("can not chose public class and active email and password", status=status.HTTP_400_BAD_REQUEST)
            if "is_password" in serializer.validated_data and serializer.validated_data["is_password"] == True and (not 'ramz' in serializer.validated_data) :
                return Response("save ramz", status=status.HTTP_400_BAD_REQUEST)


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
                    item.ramz = random.randint(1000,9999)
                    item.save()
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
        Adds the authenticated user to the public classs identified by id_class.

    Parameters:
        - id_class: ID of the classs to join.

    Response:
        - If the classs is not found, returns a 404 error.
        - If the user is already added, returns a message indicating so.
        - If the classs is not available for joining, returns an appropriate error message.
        - If successful, adds the user to the classs and reduces the stock.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class)
        except Classs.DoesNotExist:
            return Response('Class not found', status=status.HTTP_404_NOT_FOUND)
        if item.is_privet == False and item.Validation == True:
            if request.user in item.user.all():
                return Response('already added to classs', status=status.HTTP_200_OK)
            now = datetime.date.today()
            if item.start and item.start > now:
                return Response('You cannot add classs at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.finish and item.finish < now:
                return Response('You cannot add classs at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.stock and item.stock > 0:
                try:
                    with transaction.atomic():
                        item.user.add(request.user)
                        item.stock -= 1
                        item.save()
                        return Response("Added to classs", status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            elif not item.stock:
                item.user.add(request.user)
                item.save()
                return Response("Added to classs", status=status.HTTP_201_CREATED)
            else:
                return Response('classs not stock', status=status.HTTP_400_BAD_REQUEST)
        return Response(" no access ", status=status.HTTP_200_OK)





class AdduserPrivet(APIView):
    """
    API endpoint for adding users to a private classs.

    post:
        Adds a list of user IDs to the user_permissions of a private classs.

    Parameters:
        - id_class: ID of the private classs to which users are being added.

    Request body:
        - user: List of user IDs to add.

    Response:
        - If the classs is not found or the user is not authorized, returns an error.
        - If successful, adds the users to the classs.
    """
    permission_classes = [IsAuthenticated]
    def post(self,request,id_class):
        try:
            item = Classs.objects.get(teacher=request.user,id=id_class, is_privet=True)
            listuser = ListUserPrivet.objects.get(classs=item)
        except Classs.DoesNotExist:
            return Response("classs not find",status=status.HTTP_404_NOT_FOUND)
        if not request.user in item.teacher.all():
            return Response('not access' ,status = status.HTTP_403_FORBIDDEN)
        serializer = AdduserPrivetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    if listuser.is_email == True:
                        for i in serializer.validated_data['user']:
                            listuser.user.add(i)
                        l = [u.email for u in listuser.user.all()]
                        send_email_to_customer.delay(request=request.data, subject='invite',
                                                     message=f"http://127.0.0.1:8000/class/addprivete/{item.id}/{item.ramz}",
                                                     recipient_list=l)
                        return Response('add',status=status.HTTP_201_CREATED)

                    if listuser.is_password == True:
                        for i in serializer.validated_data['user']:
                            listuser.user.add(i)
                        l = [u.email for u in listuser.user.all()]
                        send_email_to_customer.delay(request=request.data, subject='invite',
                                                 message=f"password == {item.ramz}",
                                                 recipient_list=l)
                        return Response('add', status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class AddPrivatePassword(APIView):
    """

    post:
        Allows a user to join a private classs by providing the classs ID and password.

    Parameters:
        - id_class: ID of the classs to join.

    Request body:
        - password: The password required to join the classs.

    Response:
        - If the classs is not found, returns a 404 error.
        - If the password is incorrect, returns an error.
        - If the user is already added, returns a message indicating so.
        - If successful, adds the user to the classs and reduces the stock.
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
            if item.ramz != serializers.validated_data['password']:
                return Response('password not match', status=status.HTTP_400_BAD_REQUEST)
            if request.user not in listuser.user.all():
                return Response('not access', status=status.HTTP_400_BAD_REQUEST)
            if request.user in item.user.all():
                return Response('already added to classs', status=status.HTTP_200_OK)
            now = datetime.date.today()
            if item.start and item.start > now:
                return Response('You cannot add classs at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.finish and item.finish < now:
                return Response('You cannot add classs at this time', status=status.HTTP_400_BAD_REQUEST)

            if item.stock and item.stock > 0:
                try:
                    with transaction.atomic():
                        item.user.add(request.user)
                        item.stock -= 1
                        item.save()
                        return Response("Added to classs", status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            elif not item.stock:
                item.user.add(request.user)
                item.save()
                return Response("Added to classs", status=status.HTTP_201_CREATED)
            else:
                return Response('classs not stock', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPrivateEmailClass(APIView):
    """
    get id_class and key in link send to email and join classs
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,id_class,key):
        try:
            item = Classs.objects.get(id=id_class, is_privet=True, is_email=True)
            listuser = ListUserPrivet.objects.get(classs=item, is_email=True)
        except (Classs.DoesNotExist, ListUserPrivet.DoesNotExist):
            return Response('Class not found', status=status.HTTP_404_NOT_FOUND)
        if item.ramz != key:
            return Response('you not permissons join classs', status=status.HTTP_400_BAD_REQUEST)
        if request.user in listuser.user.all():
            if request.user in item.user.all():
                return Response('YOU ARE JOIND CLASS NOW', status=status.HTTP_400_BAD_REQUEST)
            now = datetime.date.today()
            if item.start and item.start > now:
                    return Response('You cannot add classs at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.finish and item.finish < now:
                    return Response('You cannot add classs at this time', status=status.HTTP_400_BAD_REQUEST)
            if item.stock and item.stock > 0:
                try:
                    with transaction.atomic():
                        item.user.add(request.user)
                        item.stock -= 1
                        item.save()
                        return Response("Added to classs", status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            elif not item.stock:
                item.user.add(request.user)
                item.save()
                return Response("Added to classs", status=status.HTTP_201_CREATED)
            else:
                return Response('classs not stock', status=status.HTTP_400_BAD_REQUEST)

        else :
            return Response('you not permissons join classs', status=status.HTTP_400_BAD_REQUEST)


class Edite(APIView):
    permission_classes = [IsAuthenticated,IsJoinable]
    def get(self, request,id_class):
        try:
            item = Classs.objects.get(id=id_class,teacher=request.user)
        except Classs.DoesNotExist:
            return Response('not found classs', status=status.HTTP_404_NOT_FOUND)

        s =ShowInfoClass(item)
        return Response(data=s.data , status=status.HTTP_200_OK)

    def put(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class, teacher=request.user)
        except Classs.DoesNotExist:
            return Response('not found classs', status=status.HTTP_404_NOT_FOUND)
        if not request.user in item.teacher.all():
            return Response('not access' ,status = status.HTTP_403_FORBIDDEN)
        serializers = Editeclass(data=request.data)
        if serializers.is_valid():
            if serializers.validated_data.get('teacher'):
                for i in serializers.validated_data['teacher']:
                    item.teacher.add(i)
                    return Response('Added to classs', status=status.HTTP_200_OK)
            if serializers.validated_data.get('ta'):
                for i in serializers.validated_data['ta']:
                    item.ta.add(i)
                    return Response(' ta Added to classs', status=status.HTTP_200_OK)
            return Response('error', status=status.HTTP_400_BAD_REQUEST)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class, teacher=request.user)
        except Classs.DoesNotExist:
            return Response('not found classs', status=status.HTTP_404_NOT_FOUND)
        if not request.user in item.teacher.all():
            return Response('not access' ,status = status.HTTP_403_FORBIDDEN)
        serializers = Editeclass(data=request.data)
        if serializers.is_valid():
            if serializers.validated_data.get('user'):
                    try:
                        user = User.objects.get(id=int(serializers.validated_data.get('user')))
                    except User.DoesNotExist:
                        return Response('user not founds', status=status.HTTP_404_NOT_FOUND)
                    if user in item.user.all():
                        item.user.remove(user)
                        return Response(f'{user.username}remove to classs', status=status.HTTP_200_OK)
                    return Response('user not found', status=status.HTTP_404_NOT_FOUND)
            return Response('error',status=status.HTTP_400_BAD_REQUEST)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)



class SubCreateClass(APIView):
    permission_classes = [IsAuthenticated,IsJoinable]
    def post(self, request,id_class):
        try:
            clas = Classs.objects.get(id=id_class)
        except  Classs.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubClass(data=request.data)
        if serializer.is_valid():
            for i in serializer.validated_data['item']:
                SubCriteriaClass.objects.create(clas=clas,name=i[0],score=int(i[1]))
            return Response ('success', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request,id_class):
            try:
                clas = Classs.objects.get(id=id_class)
            except Classs.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            sub = SubCriteriaClass.objects.filter(clas=clas)
            if sub.exists():
                try:
                    s = sub.get(name=request.data['name'])
                except SubCriteriaClass.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                s.delete()
                return Response('delete', status=status.HTTP_204_NO_CONTENT)
            return Response("not found sub", status=status.HTTP_404_NOT_FOUND)










