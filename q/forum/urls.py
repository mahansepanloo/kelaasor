from .views import *
from django.urls import path

app_name = 'forum'

urlpatterns = [
    path('questions/<int:id_class>', QuestionListCreateView.as_view(), name='question-list-create'),
    path('answers/<int:id_q>', AnswerQuestionCreateView.as_view(), name='question-detail'),
    # path('answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
    # path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
]