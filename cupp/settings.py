"""
Django settings for cupp project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

try:
    from . import local_settings as ls
except ImportError as ex:
    print(ex)
    pass


def get_local(attr_name, default_value=None):
    if hasattr(ls, attr_name):
        return getattr(ls, attr_name)
    return default_value


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9#t_q7u0jrtfbah!5h-e^krp)+gyv^yx8y+wlhdq7tz(!)6@(='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_local('DEBUG', False)

ALLOWED_HOSTS = ['*']

ADMINS = [
    ('Sansarbayar', 'sansarbayar.s@gmail.com'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'widget_tweaks',
    'corsheaders',

    'cupp.common',
    'cupp.point',
    'cupp.license',
    'cupp.event',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cupp.common.middleware.OneSessionPerUserMiddleware'
]

ROOT_URLCONF = 'cupp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cupp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_local('DB_NAME', ''),
        'USER': get_local('DB_USER', ''),
        'PASSWORD': get_local('DB_PASSWORD', ''),
        'HOST': get_local('DB_HOST', ''),
        'PORT': get_local('DB_PORT', 3306),
    }
}

# Login

SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/map/'
LOGOUT_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    }
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-US'
TIME_ZONE = 'Asia/Irkutsk'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '.store', 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '.store', 'media')

# Email

EMAIL_USE_TLS = True
EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_HOST_USER = '66a58ce90bc8df4a33c3defe85883ddf'
EMAIL_HOST_PASSWORD = '10fd3e3b0238163040a8cc0aab7d9baa'
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = 'CUPP <info@bitline.mn>'

# Format

DATE_INPUT_FORMATS = [
    '%Y/%m/%d',
    '%Y-%m-%d'
]
DATETIME_INPUT_FORMATS = [
    '%Y/%m/%d',
    '%Y/%m/%d %H:%M:%S'
]

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s [%(asctime)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '.store', 'main.log'),
            'formatter': 'simple',
            'encoding': 'utf8'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': get_local('LOGGERS', {
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'app': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }),
}

# CORS

CORS_ORIGIN_ALLOW_ALL = True