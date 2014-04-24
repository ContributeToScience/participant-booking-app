"""Production settings and globals."""

from os import environ

from base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


INSTALLED_APPS += ('gunicorn',)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
#EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
#EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
#EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
#EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
#EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
#SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://github.com/hmarr/django-ses
DEFAULT_FROM_EMAIL = 'bookingapp123@gmail.com'
AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
EMAIL_BACKEND = 'django_ses.SESBackend'
# Additionally, you can specify an optional region, like so:
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {}
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_setting('RDS_DB_NAME'),
        'USER': get_env_setting('RDS_USERNAME'),
        'PASSWORD': get_env_setting('RDS_PASSWORD'),
        'HOST': get_env_setting('RDS_HOSTNAME'),
        'PORT': get_env_setting('RDS_PORT'),
    }
}
########## END DATABASE CONFIGURATION

ALLOWED_HOSTS = [
    '54.225.90.112',
    'www.contributetoscience.org',
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

DEBUG = False

PAYPAL_RECEIVER_EMAIL = environ.get('PAYPAL_RECEIVER_EMAIL', '')
SITE_NAME = environ.get('SITE_NAME', 'booking')
PAYPAL_API_USERNAME = environ.get('PAYPAL_API_USERNAME', '')
PAYPAL_API_PASSWORD = environ.get('PAYPAL_API_PASSWORD', '')
PAYPAL_API_SIGNATURE = environ.get('PAYPAL_API_SIGNATURE', '')
PAYPAL_API_ENVIRONMENT = environ.get('PAYPAL_API_ENVIRONMENT', '')
PAYPAL_APPLICTION_ID = environ.get('PAYPAL_APPLICTION_ID', '')
PAYPAL_ACTION = environ.get('PAYPAL_ACTION', '')
PAYPAL_SERVICE = environ.get('PAYPAL_SERVICE', '')

TWILIO_ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_FROM_NUMBER = environ.get('TWILIO_FROM_NUMBER', '')
