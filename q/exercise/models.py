import datetime
from django.utils import timezone
from django.db import models
from classs.models import Classs
from accounts.models import User
from django.core.exceptions import ValidationError





class ExerciseModel(models.Model):
    classs = models.ForeignKey(Classs, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    description = models.TextField()
    limit_time = models.DateTimeField(null=True, blank=True)
    limit_send = models.IntegerField(null=True, blank=True)
    score = models.IntegerField()
    nsocre = models.IntegerField(null=True,blank=True)
    is_group = models.BooleanField(default=False)
    answer_format = models.CharField(
        max_length=10,
        choices=[
            ('1', 'Text Response'),
            ('2', 'File Upload'),
            ('3', 'Judged Code Submission')
        ]
    )
    penalty_time = models.IntegerField(null=True, blank=True)
    penalty_score = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)



    def save(self, *args, **kwargs):
        self.nscore = self.score
        super().save(*args, **kwargs)



class Test(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    exercise = models.ForeignKey(ExerciseModel,on_delete=models.CASCADE)
    inputs = models.TextField()
    outputs = models.TextField()



class Group(models.Model):
    exercise = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE, related_name='exercisegroup')
    user = models.ManyToManyField(User)

class SubCriteria(models.Model):
    exercise = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE, related_name='subcriteria')
    name = models.CharField(max_length=100)
    score = models.FloatField()

    def clean(self):
        if self.score <= self.exercise.score:
            self.exercise.score -= self.score
        return ValidationError('score cannot be less than')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



class AnswersModel(models.Model):  # ملاک اصلی ما
        exercise = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE, related_name="eanswers")
        text = models.TextField(null=True, blank=True)
        file = models.FileField(null=True, blank=True,upload_to='media')
        juge = models.TextField(null=True, blank=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
        group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='ganswer', null=True, blank=True)
        score_received = models.IntegerField(null=True, blank=True)
        bazkhord = models.TextField(null=True,blank=True)

        def save(self, *args, **kwargs):
            now = timezone.now()
            if self.exercise.limit_time:
                if self.exercise.limit_time <= now:
                    if self.exercise.penalty_time is None or self.exercise.penalty_time == 0:
                        self.exercise.available = False
                        self.exercise.save()
                        raise ValidationError("can not answer ")
                    else:
                        self.exercise.limit_time += datetime.timedelta(days=self.exercise.penalty_time)
                        if self.exercise.penalty_score:
                            self.exercise.score -= (self.exercise.penalty_score * self.exercise.score) / 100
                            self.exercise.save()


            if not self.exercise.available:
                raise ValidationError("can not answer")

            super().save(*args, **kwargs)


from django.db.models import Sum

class Socer(models.Model):#امتیاز نهایی
    classs = models.ForeignKey(Classs, on_delete=models.CASCADE, related_name='socer', null=True, blank=True)
    exercises = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_received = models.IntegerField(null=True, blank=True)
    limit = models.IntegerField(default=0)

    def total_score(self):
        return Sum(self.score_received)


    def save(self, *args, **kwargs):
        self.classs = self.exercises.classs
        super(Socer, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username




class RezScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urez')
    sub = models.ForeignKey(SubCriteria, on_delete=models.CASCADE, related_name='srez')
    score = models.IntegerField()



class InboxExerciseModel(models.Model):
    exercise = models.ForeignKey(ExerciseModel,on_delete=models.CASCADE,related_name="ei")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class GroupAssignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_assignments')
    score_received = models.FloatField(null=True, blank=True)

