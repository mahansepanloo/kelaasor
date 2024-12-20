from .views import *
from django.urls import path

app_name = 'forum'

urlpatterns = [
    path('questions/<int:id_class>', QuestionListCreateView.as_view(), name='question-list-create'),
    path('answers/<int:id_q>', AnswerQuestionCreateView.as_view(), name='question-detail'),
    path('answer/<int:id_a>/<int:id_q>', Replyanswer.as_view(), name='reply-detail'),
    path('ShowQ/<int:id_class>/<int:id_q>', ShowQ.as_view(), name='ShowQ'),
    path('editanswer/<int:id_a>/<int:id_class>', EditeAnswer.as_view(), name='answer-detail'),
]