from celery import shared_task
from django.core.mail import send_mail
from portfolio import settings

from .models import Feedback
from datetime import datetime, timedelta

# background task to send mails
@shared_task(bind=True)
def send_email(self, email_id):
    mail_subject = f"Hi {email_id.split('@')[0]}"
    html_message = """
    Thank You, for your feedback!! If required I will contact you soon.
    Do check my GitHub@vallabhtiwari(https://github.com/vallabhtiwari)
    
    Vallabh Tiwari
    """
    to_email = email_id
    send_mail(
        subject=mail_subject,
        message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )


# background task to delete feedbacks older than 10 days
@shared_task(bind=True)
def delete_feedbacks(self):
    current = datetime.now()
    delta = timedelta(days=10)  # timedelta for 10days
    Feedback.objects.filter(date_created__lte=current - delta).delete()
