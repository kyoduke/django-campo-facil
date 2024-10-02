from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def send_mail_task(
    subject,
    message,
    recipient_list,
    html_message=None,
):
    logger.info("Sent email")
    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "EMAIL_HOST_USER", None),
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message,
    )
