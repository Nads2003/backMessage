import os
from pathlib import Path
from datetime import timedelta
import urllib.parse

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY & DEBUG
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
DEBUG = ENVIRONMENT != "production"


if ENVIRONMENT == "production":
    ALLOWED_HOSTS = [
        ".railway.app",
    ]
else:
    ALLOWED_HOSTS = ["*"]
 # Remplace par ton domaine Railway/Netlify si tu veux
if ENVIRONMENT == "production":
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Applications
INSTALLED_APPS = [
    'daphne',   # Obligatoire pour ASGI
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    'rest_framework',
    'channels',

    'accounts',
    'friends',
    'chat',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASE_URL = os.environ.get("DATABASE_URL")

if ENVIRONMENT == "production" and DATABASE_URL:
    result = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": result.path[1:],
            "USER": result.username,
            "PASSWORD": result.password,
            "HOST": result.hostname,
            "PORT": result.port,
            "CONN_MAX_AGE": 600,
            "OPTIONS": {
                "sslmode": "require",
            },
        }
    }

else:
    # ===== LOCAL =====
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "messagerie_db",
            "USER": "postgres",
            "PASSWORD": "sambatra",
            "HOST": "localhost",
            "PORT": 5432,
        }
    }


# Auth
AUTH_USER_MODEL = 'accounts.Utilisateur'

# REST Framework + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Channels (WebSocket)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")],
        },
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# CORS & CSRF
CORS_ALLOW_ALL_ORIGINS = False
if ENVIRONMENT == "production":
    CORS_ALLOWED_ORIGINS = [
        "https://chat-messag.netlify.app",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://chat-messag.netlify.app",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
    ]

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
