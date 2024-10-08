from  django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from classs.email import sendemail


@receiver(post_save, sender=ExerciseModel)
def notify_class_users(sender, instance, created, **kwargs):
    users = instance.classs.user.all()
    subject = f"Exercise {'Created' if created else 'Updated'}"
    message = f"The exercise '{instance.name}' has been {'created' if created else 'updated'}. Please check it."
    email_from = "msepanloooo@gmail.com"

    for user in users:
        sendemail(subject, message, email_from, [user.email])


