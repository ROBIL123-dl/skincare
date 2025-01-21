"""
Django settings for lushaura project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import pdfkit
from pathlib import Path
from environ import Env
env = Env()
Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

WKHTMLTOPDF_CMD = r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG',default=False)

ALLOWED_HOSTS = []
SITE_ID=env.int('SITE_ID')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_management',
    
    'django.contrib.sites',#cross/app for connect with multiple website
    'allauth',# django authentication app
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', #app is provider for social authentication
    
    'customer',
    'vendor'
    
    
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',               #for authentication
    'allauth.account.auth_backends.AuthenticationBackend'
 ]

MIDDLEWARE = [
   
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    
]

ROOT_URLCONF = 'lushaura.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templete'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ], 
        },
    },
]

WSGI_APPLICATION = 'lushaura.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE':'django.db.backends.postgresql',
        'NAME': env('NAME'),     
        'USER': env('USER'),         #env varible for database connection
        'PASSWORD':env('PASSWORD'),    
        'HOST':env('HOST'),             
        'PORT':env('PORT'),
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =env('EMAIL_HOST') # Use your email provider's SMTP server
EMAIL_PORT =env.int('EMAIL_PORT')                                                            #env varible for emal authentication
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD =env('EMAIL_HOST_PASSWORD') 

RAZORPAY_KEY_ID ='rzp_test_EJf0dXqL1Vhov0'     #env('RAZORPAY_KEY_ID')         # rasorpay integreation keys
RAZORPAY_KEY_SECRET='6aNkHfwsj0DSqfaNQyiTpDXw'    #env('RAZORPAY_KEY_SECRET')

SECURE_CROSS_ORIGIN_OPENER_POLICY="same-orgin-allow-popups"
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = 'static/'
STATICFILES_DIRS = [           # env varible for static folders
    BASE_DIR/"static"
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'   # env varible for media folder

AUTH_USER_MODEL = 'user_management.User'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',  # Ensures email is requested
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

LOGIN_REDIRECT_URL='c_home'
LOGOUT_REDIRECT_URL='index'
SOCIALACCOUNT_LOGIN_ON_GET=True







# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

