from django.core.mail import send_mail
from django.conf import settings

def sendemail(request, sub : str, messages : str, recipient_list : list):
    subject = sub
    message = messages
    email_from = settings.EMAIL_HOST_USER
    recipient_list = recipient_list
    send_mail(subject, message, email_from, recipient_list)
