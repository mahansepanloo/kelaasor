from .views import *
from django.urls import path

app_name = 'forum'

urlpatterns = [
    path('questions/<int:id_class>', QuestionListCreateView.as_view(), name='question-list-create'),
    path('answers/<int:id_q>', AnswerQuestionCreateView.as_view(), name='question-detail'),
    path('ShowQ/<int:id_class>/<int:id_q>', ShowQ.as_view(), name='ShowQ'),
    # path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
]