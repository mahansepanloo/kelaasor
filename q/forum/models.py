from django.db import models
from accounts.models import User
from classs.models import Classs
from django.core.validators import MaxValueValidator,MinValueValidator


class Question(models.Model):
    classs = models.ForeignKey(Classs,on_delete=models.CASCADE,related_name='cquestions')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uquestions')
    title = models.CharField(max_length=1000)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='qanswer')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='ranswer',null=True,blank=True)
    is_reply = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uanswer')
    answers = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    class Meta:
        ordering = ('-rate',)


    # def average_rate(self):
    #     rates = self.rrate.all()
    #     total = sum(rate.get_rate() for rate in rates)
    #     count = rates.count()
    #     return total / count if count > 0 else 0



# class Rate(models.Model):
#     answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='rrate')
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='urate')
#     rate = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)],default=0)
#     def get_rate(self):
#         return self.rate




class Rate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rrate')
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='rrate')