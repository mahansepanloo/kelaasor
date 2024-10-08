from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer
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
        return serializer.save(classs_id=self.kwargs.get('id_class'),user=self.request.user)

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












