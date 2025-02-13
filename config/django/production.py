from .base import *  # noqa: F403
import dj_database_url
from config.env import env

DEBUG = env.bool('DJANGO_DEBUG', default=False)


ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[]) + ["127.0.0.1", "[::]", "localhost"]

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[]) + [ "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:4000", "http://127.0.0.1:4000"]

# CORS
CORS_ALLOW_ALL_ORIGINS = True # TODO: Remove this in production please, and add the correct origins

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",     # React default port
#     "http://127.0.0.1:3000",
#     "http://localhost:8080",     # Vue.js default port
#     # Add your frontend domains here
#     # "https://yourdomain.com",
# ]

DATABASES = {
    "default": dj_database_url.parse(
        env.str('DATABASE_URL'), conn_max_age=600, conn_health_checks=True
    )
}

REDIS_URL = env.str("REDIS_URL")

# EMAIL CONFIGURATION (PRODUCTION)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str("MAILER_SMTP_HOST")
EMAIL_PORT = env.bool("MAILER_SMTP_PORT")
EMAIL_USE_TLS = env.bool("MAILER_SMTP_TLS")
EMAIL_HOST_USER = env.str("MAILER_SMTP_USER")
EMAIL_HOST_PASSWORD = env.str("MAILER_SMTP_PASSWORD")
DEFAULT_FROM_EMAIL = "User <no-reply@django-rest-boiler-plate-template.com>"
