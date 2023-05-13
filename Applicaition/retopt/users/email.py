from django.core.mail import send_mail
from django.conf import Settings

def send_otp_via_email(email, otp_obj):
    subject = 'Youre Account Verification email'
    message = f'Your otp is {otp_obj.code}'
    email_from = Settings.EMAIL_HOST
    email_to = email
    send_mail(subject, message, email_from, email_to)