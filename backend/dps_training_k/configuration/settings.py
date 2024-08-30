"""
Django settings for dps_training_k project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

from environ import Env

from helpers import DateTimeNameGenerator
from .config import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# import env file
env = Env()
Env.read_env(os.path.join(BASE_DIR, ".env.dev"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOWED_ORIGINS = ["https://klinik-dps.de", "https://www.klinik-dps.de", "http://localhost"]
RUN_CONFIG = env.str("RUN_CONFIG", default="dev")

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]

SECRET_KEY = env.str("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
INTERNAL_IPS = env.list("INTERNAL_IPS", None)

# Application definition

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "game.apps.GameConfig",
    "helpers.apps.GameConfig",
    "template.apps.TemplateConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "django_celery_beat",
    "django_celery_results",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "configuration.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "configuration.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# ToDo: replace with env.db() : https://django-environ.readthedocs.io/en/latest/api.html
DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CHANNEL_LAYERS = {
    "default": (
        {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [
                    env.str("REDIS_URL", default="redis://localhost:6379")
                ]  # for production
            },
        }
        if env.bool("CHANNEL_REDIS", False)
        else {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    )
}
DEFAULT_NAME_GENERATOR = DateTimeNameGenerator()

AUTH_USER_MODEL = "game.User"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Celery
# ------------------------------------------------------------------------------
# See: http://docs.celeryproject.org/en/latest/userguide/configuration.html
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env.str("REDIS_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60  # TODO: Change if necessary
CELERY_TASK_SOFT_TIME_LIMIT = 60  # TODO: Change if necessary

CELERY_BEAT_SCHEDULE = {
    "update_patients": {
        "task": "game.tasks.check_for_updates",
        "schedule": 1.0,
    },
}

DATA_ROOT = os.path.join(BASE_DIR, "data")

# Redis connection settings
REDIS_HOST = "K-dPS-redis"
REDIS_PORT = 6379
REDIS_DB = 0

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug.log'),
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
