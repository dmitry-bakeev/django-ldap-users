import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'edit-in-local_settings.py'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # Standart
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External libraries
    # Local
    'users',
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

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
        ],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LEN = 255
SHORT_LEN = 127


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    STATIC_DIR,
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Media

MEDIA_URL = '/media/'


# Auth

AUTH_USER_MODEL = 'users.User'

LOGOUT_REDIRECT_URL = 'users:login'
LOGIN_URL = 'users:login'

# Auth backend
AUTHENTICATION_BACKENDS = (
    'users.backends.DomainModelBackend',
    'users.backends.LDAPModelBackend',
)

# Like choices to model field ('value-to-save-in-db', 'display-value')
# Example
# Set your values in local_settings.py
DOMAIN_CHOICES = (
    ('domain_1', 'Domain_1'),
    ('domain_2', 'Domain_2'),
    ('domain_n', 'Domain_n'),
)

# This SEPARATE_CHARACTER is using to separate domain and username in User.username field
# Do not edit this after creating users, because it broken all user's accounts
SEPARATE_CHARACTER = '?'

# If your DOMAIN_CHOICES contains DOMAIN_SUPERUSER change this value to another in local_settings.py
# ATTENTION: This param store in db after creating a superuser
# If you change this value you can loss superuser's account
DOMAIN_SUPERUSER = 'super'

# For each domain in DOMAIN_CHOICES need to set URI, DN, DOMAIN
# Example
# Set your values in local_settings.py
AUTH_LDAP_SERVERS = {
    'domain_1': {
        'URI': '127.0.0.1',  # domain_1 IP
        'DN': 'dc=domain_1,dc=com',
        'DOMAIN': 'domain_1.com'
    },
    'domain_2': {
        'URI': '127.0.0.1',  # domain_2 IP
        'DN': 'dc=domain_2,dc=com',
        'DOMAIN': 'domain_2.com'
    },
    'domain_n': {
        'URI': '127.0.0.1',  # domain_n IP
        'DN': 'dc=domain_n,dc=com',
        'DOMAIN': 'domain_n.com'
    },
}

# Automatic user account conform on first login via LDAP
AUTO_CONFIRM_USER = False


# Load local settings

try:
    from .local_settings import *  # noqa: F401, F403
except ImportError:
    pass
