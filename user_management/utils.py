import pyotp
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import User
from django.conf import settings 


def generate_otp():
      secret = pyotp.random_base32()
      totp = pyotp.TOTP(secret, interval=120)      #funtion for generate otp
      otp = totp.now()
      return otp

def verify_otp(otp,user_otp):
    print(f'single:{otp},secrete{user_otp}')
    print(otp == user_otp)                        #funtion for verify otp
    print(type(otp), type(user_otp))
    return otp == user_otp

def email(user):
    print('test email')
    user=User.objects.get(id=user)
    email_otp = generate_otp()                   #funtion for send email
    print(email_otp)
    user.otp=email_otp
    user.save()
   
    send_mail(
        
            'Email Verification OTP',
            f'Your OTP for email verification is: {email_otp}',
            settings.EMAIL_HOST_USER,                         # send email email authentication
            recipient_list=[user.email],
            fail_silently=False,
           )
    return True


def approval_email(vender,text):
    if text == None: 
        send_mail(
        
            'Welcome to Lushaura',
            f'Approved {vender.full_name} registration,Please Try to sell your product ,Thank You',
            settings.EMAIL_HOST_USER,                            # send email approved
            recipient_list=[vender.email],
            fail_silently=False,
            )
    else:    
      send_mail(
        
            'Welocme to Lushaura',
            f'Not approved {vender.full_name} registration:{text}',
            settings.EMAIL_HOST_USER,                            # send email not approved
            recipient_list=[vender.email],
            fail_silently=False,
            )
    return True