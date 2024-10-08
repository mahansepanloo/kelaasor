from django.db import models
from accounts.models import User
from classs.models import Classs



class Question(models.Model):
    classs = models.ForeignKey(Classs,on_delete=models.CASCADE,related_name='cquestions')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uquestions')
    title = models.CharField(max_length=1000)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='qanswer')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uanswer')
    answers = models.TextField()
    replay = models.ForeignKey('self',on_delete=models.CASCADE,related_name='areplay',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


