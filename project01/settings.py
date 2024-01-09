"""
Django settings for project01 project.

Generated by 'django-admin startproject' using Django 3.2.23.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from firebase_admin import initialize_app

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p&mlwbmxykb$li)4vv%%fq2fxctvww3!%3at0=qrsn(6+1_td&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',
    'google_translate',
    "fcm_django",
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'blog',
    'polls',
    'django_filters',
    'ckeditor',
]
SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET=True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'polls.middleware.CustomErrorMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect

ROOT_URLCONF = 'project01.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'project01.wsgi.application'
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
REST_FRAMEWORK = {
     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}



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
AUTHENTICATION_BACKENDS = [
    'blog.authentication_backends.EmailOrUsernameModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '196069865532-u13ekuhp0e3k6cr596cl1kd96kg0g433.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
     'github': {
        'APP': {
            'client_id': 'Iv1.10a540fa2776df8c',
            'secret': '266f61abdd44813cd9d075ae4f175cfd1cb28dfb',
            'key': '',
        },
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
     'linkedin_oauth2': {
         'APP': {
            'client_id': '77wvscmxfqbk1m',
            'secret': 'a3dRUGRhWJe3JfI5',
            'key': '',
        },
          'SCOPE': [
            'r_liteprofile',
            'r_emailaddress',
            'w_member_social',
        ],
         'PROFILE_FIELDS': [
            'id',
            'firstName',
            'lastName',
            'emailAddress',
            'email-address',
            'profilePicture',
            'public-profile-url',
        ],
        'LOCATION_FIELDS': [
            'location',
        ],
        'POSITION_FIELDS': [
            'company',
        ]
    },
      'facebook': {
       'callbackURL'   : 'http://127.0.0.1:8000/accounts/facebook/login/callback/',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
    }
}
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '77wvscmxfqbk1m'  # App ID
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET ='a3dRUGRhWJe3JfI5'
firebase_config = {
    "apiKey": "AIzaSyDbKj0Tom9CzZ66N3O9UfkPyXr0r505-VE",
    "authDomain": "django-fcm-8e2f0.firebaseapp.com",
    "projectId": "django-fcm-8e2f0",
    "storageBucket": "django-fcm-8e2f0.appspot.com",
    "messagingSenderId": "196069865532",
    "appId": "1:196069865532:web:88f22c137bd5977519eb39",
    "measurementId": "G-Z1EJE6FK4Z",
}
firebase_credentials_path = r'C:\Users\chira\Desktop\django-merged\firebase-service-account-key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = firebase_credentials_path
FIREBASE_APP = initialize_app(options={
    'projectId': firebase_config['projectId'],
    'credential_path': firebase_credentials_path,
    # Add other configuration options if necessary
})
FCM_DJANGO_SETTINGS = {
    "DEFAULT_FIREBASE_APP": FIREBASE_APP,
    "ONE_DEVICE_PER_USER": False,  # Set to True if you want only one active device per user at a time
    "DELETE_INACTIVE_DEVICES": False,  # Set to True if you want to delete inactive devices
}
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

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'post_list' 
# LOGIN_URL = '/login/'
AUTH_USER_MODEL = 'blog.CustomUser'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')