
from pathlib import Path
from corsheaders.defaults import default_headers
from dotenv import load_dotenv
import os
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('API_SECRET_KEY')

USER_SECRET_KEY = os.getenv('USER_MANAGEMENT_SECRET_KEY')

# DEBUG ayarı (bool olarak okuma)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS ayarı (virgül ile ayrılan stringi listeye çevir)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# SERVICE_ROUTES ortam değişkenini JSON formatında oku
# SERVICE_ROUTES işlevi, API isteklerini doğru mikroservise yönlendirmektir
# hangi URL'nin hangi servise yönlendirileceği tanımlanıyor. Bu bölümde, her mikroservisin kendine ait bir yolu var.
# users/ : Tüm users ile başlayan istekler usermanagement servisine yönlendirilir.
# game/ : Oyun servisiyle ilgili olan istekler game_service servisine gider.
# friend/ : Arkadaş yönetimiyle ilgili istekler friend_servicee yönlendirilir.

SERVICE_ROUTES = {
  "users/": "http://usermanagementc:8000",
  "game/": "http://game_service:8001",
  "friend/": "http://friend_service:8002"
}

import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'apigateway.log',
        },
    },
    'loggers': {
        'apigateway': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# settings.py
# Django Rest Framework ayarları
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Varsayılan olarak JSON yanıt
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Varsayılan olarak JSON veri alma
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # Diğer kimlik doğrulama yöntemlerini buraya ekleyebilirsiniz.
    ],
}

# Standart Django ayarları
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST framework
    'corsheaders',  # CORS ayarları için
    'routes',  # API yönlendirme uygulaması
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'routes.middleware.JWTAuthenticationMiddleware',  # JWT doğrulama middleware
]

CORS_ALLOW_ALL_ORIGINS = True  # Geliştirme aşamasında tüm kaynaklara izin veriyoruz

#cors headers
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'id',  # Özel başlığınız
]
CORS_ALLOW_ALL_HEADERS = True

# settings.py


ROOT_URLCONF = 'apigateway.urls'

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

WSGI_APPLICATION = 'apigateway.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
