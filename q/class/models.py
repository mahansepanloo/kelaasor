from django.db import models
from accounts.models import User


class Classs(models.Model):
    CLASS_TYPE_CHOICES = [
        ('1', 'Public'),
        ('2', 'Private')
    ]
    type = models.CharField(max_length=20, choices=CLASS_TYPE_CHOICES)
    teacher = models.ManyToManyField(User,related_name='tclass')
    ta = models.ManyToManyField(User,related_name='taclass',null=True,blank=True)
    user = models.ManyToManyField(User,related_name='uclass',blank=True,null=True)
    is_privet = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    is_password = models.BooleanField(default=False)
    Validation = models.CharField(max_length=10000,null=True,blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)
    start = models.DateField(null=True,blank=True)
    finish = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.name} - {self.id}"


class ListUserPrivet(models.Model):
    classs = models.ForeignKey(Classs,on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    is_email = models.BooleanField(default=False)
    is_password = models.BooleanField(default=False)
