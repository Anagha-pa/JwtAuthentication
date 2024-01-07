from django.core.mail import send_mail
import random
from django.conf import settings
from .models import UserData


def send_otp_via_email(email):
    subject = 'Your account verification email'
    otp = random.randint(1000,9999)
    message = f'Your otp is {otp}'
    email_form = settings.EMAIL_HOST
    send_mail(subject,message,email_form,[email])
    user_obj = UserData.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()



def send_forgot_password_mail(email,token):
    subject = "Your forgotpassword link"
    message = f'Hii , click on the link to reset your password http://localhost:8000/api/account/reset-password/{token}/'
    email_from = settings.EMAIL_HOST_USER  
    send_mail(subject,message,email_from,[email])
    return True