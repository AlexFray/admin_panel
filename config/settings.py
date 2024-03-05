import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include as include_settings

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

include_settings(
    "components/database.py",
    "components/installed_apps.py",
    "components/middleware.py",
    "components/password_validators.py",
    "components/templates.py",
)

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", False) == "True"
ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS")]
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE")

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8080",]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = "/home/alex/projects/new_admin_panel_sprint_1/movies_admin/static"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': False,
        }
    },
}
