
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from threading import Thread

def send_confirmation_email(subject, message, recipient_list):

    email_from = settings.EMAIL_HOST_USER
    
    def th():
       send_mail(subject, message, email_from, recipient_list)
    
    Thread(target=th).start()