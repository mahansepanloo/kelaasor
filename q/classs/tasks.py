from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, default_retry_delay=10, max_retries=10)
def send_email_to_customer(self, request,subject: str, message: str, recipient_list: list):
    try:
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {e}")
        raise self.retry(exc=e)

