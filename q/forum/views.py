from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer,Rate
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.views import APIView
from .permissions import *

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsJoinable]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['created_at']
    search_fields = ['title', 'question_text']

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title', serializer.validated_data.get('question_text')[0:20])
        return serializer.save(classs_id=self.kwargs.get('id_class'),user=self.request.user,title=title)

    def get_queryset(self):
        id_class = self.kwargs.get('id_class')
        return self.queryset.filter(classs_id=id_class)


class AnswerQuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_q):
        item = Question.objects.get(pk=self.kwargs.get('id_q'))
        if (self.request.user in item.classs.teacher.all() or self.request.user in item.classs.ta.all() or
                self.request.user in item.classs.user.all()):
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(question=item, user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('not accessible', status=status.HTTP_400_BAD_REQUEST)

class EditeAnswer(APIView):
    permission_classes = [IsAuthenticated, IsJoinable]
    def put(self,request,id_a,id_class):
        item = Answer.objects.get(id=id_a)
        if request.user == item.user or request.user in item.question.classs.teacher.all() or request.user in item.question.classs.ta.all():
            serializer = AnswerSerializer(instance=item,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('nor accesss')    

    def delete(self,request,id_a,id_class):
        item = Answer.objects.get(id=id_a)
        if request.user == item.user or request.user in item.question.classs.teacher.all() or request.user in item.question.classs.ta.all():
            item.delete()
            return Response('deleted', status=status.HTTP_200_OK)
        return Response('nor accesss')    
    

class Replyanswer(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id_a,id_q):
        item = Question.objects.get(pk=self.kwargs.get('id_q'))
        if (self.request.user in item.classs.teacher.all() or self.request.user in item.classs.ta.all() or
                self.request.user in item.classs.user.all()):
            answers = Answer.objects.get(question = item, id = id_a)
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(question=item, user=self.request.user, is_reply = True, reply = answers)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('not accessible', status=status.HTTP_400_BAD_REQUEST)




class ShowQ(APIView):
    permission_classes = [IsAuthenticated, IsJoinable]
    def get(self, request,id_class,id_q):
        item = Answer.objects.filter(question_id=id_q)
        serializer = AnswerSerializer(instance=item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request,id_class,id_q):
        item = Answer.objects.get(question_id=id_q,id=request.data.get('id'))
        try:
            f = Rate.objects.get(answer = item, user = request.user )
            return Response('can not rate')
        except Rate.DoesNotExist:
            Rate.objects.create(answer=item, user=request.user)
            item.rate += 1
            item.save()
            serializer = AnswerSerializer(instance=item)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,id_class,id_q):
        item = Answer.objects.get(question_id=id_q, id=request.data.get('id'))
        try:
            f = Rate.objects.get(answer=item, user=request.user)
            f.delete()
            item.rate -= 1
            item.save()
            serializer = AnswerSerializer(instance=item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Rate.DoesNotExist:
            return Response("can not delete")











