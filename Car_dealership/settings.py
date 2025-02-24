

from pathlib import Path
import os
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-kq$@gg^^h#hf7ci-^a5y3)vj1e8i1jpoa8-$&vr$c#q*sd+!uh'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
      'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'CAR',
    'rest_framework',
    'corsheaders',
    'paypal.standard.ipn'
]

# PayPal Settings
PAYPAL_RECEIVER_EMAIL = "your-paypal-business-email@example.com"
PAYPAL_TEST = True  # Change to False in production


#CORS_ALLOW_ALL_ORIGINS = True #to be changed
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "Authorization",
    "Content-Type",
]
ALLOWED_HOSTS = [
    '40d4-41-89-243-5.ngrok-free.app',
    '127.0.0.1',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",  # Add your frontend URL here
]

CSRF_TRUSTED_ORIGINS = [
    'https://40d4-41-89-243-5.ngrok-free.app',
    "http://127.0.0.1:3000",
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_COOKIE": "access_token",  # Cookie name
    "AUTH_COOKIE_HTTP_ONLY": True,  # Prevent JavaScript access
    "AUTH_COOKIE_SECURE": True,  # Set to False for development, True for production (HTTPS)
    "AUTH_COOKIE_SAMESITE": "Lax",  # Prevent CSRF attacks
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Car_dealership.urls'

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

WSGI_APPLICATION = 'Car_dealership.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'Car-web-app',
#        'USER': 'pioneer',
#        'PASSWORD': '**********',
#        'HOST': 'localhost',  
#        'PORT': '5432',
#}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
AUTH_USER_MODEL = 'CAR.User'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
      "topmenu_links" : [
            {"name": "Support", "url": "https://github.com/joseph-tech-dev/car-web-app#","new_window": True}
      ],
      "copyright": "HotwheelsHQ",
      "site_title": "HotwheelsHQ",
      "site_header": "HotwheelsHQ",
      "welcome_sign": "Welcome to HotwheelsHQ",
      "site_logo": "logo.jpeg",
      "site_logo_classes": "img-circle",
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-warning",
    "accent": "accent-indigo",
    "navbar": "navbar-warning navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "simplex",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Work on login logic,
# Work on remain front-ends