"""
Django settings for irrigation project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from mysettings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'agenda.apps.AgendaConfig',
    'notification.apps.NotificationConfig',
    'dashboard.apps.DashboardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'irrigation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.views.custom_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'irrigation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


LOGOUT_REDIRECT_URL = '/'

# email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'irrigator.it@gmail.com'
EMAIL_HOST_PASSWORD = PASSWORD_GMAIL
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True



PLANT = 'cover/balcony.jpg'
TERRACE = 'cover/terrace.jpg'
FLOWER = 'cover/flower.jpg'
GARDEN = 'cover/garden.jpg'
VEGETABLE = 'cover/vegetable.jpg'
IMG_CHOICES = (
    (PLANT, 'Pianta'),
    (TERRACE, 'Albero'),
    (GARDEN, 'Prato'),
    (VEGETABLE, 'Verdura'),
    (FLOWER, 'Fiore'),
)

MANUAL = 'M'
CALENDAR = 'C'
SMART = 'S'
IRRIGATION = [
    (MANUAL, 'Manuale'),
    (CALENDAR, 'Programmata'),
    (SMART, 'Intelligente'),
]

FREQUENCY = [
    ('0', 'ogni giorno'),
    ('1', 'giorni alterni'),
    ('2', 'ogni 2 giorni'),
    ('3', 'ogni 3 giorni'),
    ('4', 'ogni 4 giorni'),
    ('5', 'ogni 5 giorni'),
    ('7', 'una volta a settimana'),
    ('10', 'ogni 10 giorni'),
    ('14', 'una volta ogni due settimane'),
]

DURATION = [
    '1 minuto ', '2 minuti ', '3 minuti ', '4 minuti ', '5 minuti ', '6 minuti ', '7 minuti ', '8 minuti ', '9 minuti ',
    '10 minuti ', '11 minuti ', '12 minuti ', '13 minuti ', '14 minuti ', '15 minuti ', '20 minuti ', '25 minuti ',
    '30 minuti ', '40 minuti ', '30 minuti ', '45 minuti ',
    '50 minuti ', '55 minuti ', '60 minuti ',
]
