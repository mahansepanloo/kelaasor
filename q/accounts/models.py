from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.db import models
from django.contrib.postgres.fields import ArrayField




class User(AbstractUser,PermissionsMixin):
    phone_number = models.CharField(max_length=11)
    avabelle_email = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


