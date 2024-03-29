"""
Django settings for mkt_blend project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-upzr4x-#n41i7@gikx8d4+)z#do$=1-h2h2rc8^0g7)v$#-o59'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ["talentcommunity-env.eba-fqgc5ip5.us-east-1.elasticbeanstalk.com"]
ALLOWED_HOSTS = ["tct.blend360dev.io", 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bios.apps.BiosConfig',
    'user',
    # ms azure
    'django_auth_adfs',

    # sso admin
    'admin_sso',

    # plotly dash
    # 'django_plotly_dash.apps.DjangoPlotlyDashConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ms azure
    'django_auth_adfs.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'mkt_blend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # changed
        # 'DIRS': [os.path.join(BASE_DIR, 'bios/templates')],
        'DIRS': [],
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

WSGI_APPLICATION = 'mkt_blend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'bios/static/media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bios/static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# ms azure
AUTHENTICATION_BACKENDS = (
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'admin_sso.auth.DjangoSSOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',    
)

# client_id = '1602ed5b-59e1-4cbc-a040-ba579351ff72'
# client_secret = 'iwi7Q~-E4mnG.6hxBSC~R~FpPSz9b7u4rVJyf'
# tenant_id = 'b1aae949-a5ef-4815-b7af-f7c4aa546b28'

client_secret = ''
client_id = ''
tenant_id = ''

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = ''
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = ''


AUTH_ADFS = {
    'AUDIENCE': client_id,
    'CLIENT_ID': client_id,
    'CLIENT_SECRET': client_secret,
    'CLAIM_MAPPING': {'first_name': 'given_name',
                      'last_name': 'family_name',
                      'email': 'upn'},
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'upn',
    'TENANT_ID': tenant_id,
    'RELYING_PARTY_ID': client_id,
    "LOGIN_EXEMPT_URLS": ["api/", "public/"],
}

LOGIN_URL = '/oauth2/login' 
LOGIN_REDIRECT_URL = '/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

