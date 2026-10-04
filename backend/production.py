from .settings import *  # noqa: F403
import dj_database_url
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# nginx posílá /api/* na backend a prefix odřízne; Django ho tak musí
# přidávat zpět do generovaných URL (redirecty, admin, reverse())
FORCE_SCRIPT_NAME = '/api'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
