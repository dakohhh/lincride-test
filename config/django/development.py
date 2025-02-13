from .base import *  # noqa: F403
from config.env import env, BASE_DIR

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ["*"]


# CORS
CORS_ALLOW_ALL_ORIGINS = True 

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REDIS_URL = "redis://localhost:6379/0"

# EMAIL CONFIGURATION (DEVELOPMENT)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_USE_TLS = False
EMAIL_PORT = 2525
EMAIL_HOST_USER = "user"
EMAIL_HOST_PASSWORD = "pass"
DEFAULT_FROM_EMAIL = "User <no-reply@django-rest-boiler-plate-template.com>"
