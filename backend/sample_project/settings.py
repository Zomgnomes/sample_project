"""
Django settings for Sample Project project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import secrets

import environ

ROOT_DIR = environ.Path(__file__) - 2

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
]

LOCAL_APPS = [
    "apps.users",
    "apps.data",
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "apps.users.middleware.HealthCheckMiddleware",
]

# This is set on every request, and determines what information and level of info (path, origin, etc.) to send back
# in the response header. See https://docs.djangoproject.com/en/4.0/ref/middleware/#referrer-policy-1
# and https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy for a detailed discussion
SECURE_REFERRER_POLICY = env.str(
    "SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin"
)

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY", default=secrets.token_urlsafe(60))

# DOMAINS
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
DOMAIN = env.str("DOMAIN")
FRONTEND_URL = env.str("FRONTEND_URL")

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_PORT = env.int("EMAIL_PORT", default="1025")
EMAIL_HOST = env.str("EMAIL_HOST", default="mailhog")

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("Alex Smith", "z@omg.nom.es"),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST", "postgres"),
        "PORT": 5432,
    },
}

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/staticfiles/"


# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(ROOT_DIR("static")),
    str(ROOT_DIR("sample_project/templates")),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

LOCAL_HOST = env.bool("LOCAL_HOST", False)

if LOCAL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    DEFAULT_FILE_STORAGE = "sample_project.storage_backends.MediaStorage"
    STATICFILES_STORAGE = "sample_project.storage_backends.StaticStorage"
    STATIC_URL = "/static/"

    AWS_S3_REGION_NAME = "us-east-2"
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_QUERYSTRING_EXPIRE = 28800
    AWS_AUTO_CREATE_BUCKET = True
    AWS_S3_USE_SSL = True
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    # Email Settings
    EMAIL_BACKEND = "django_ses.SESBackend"
    AWS_SES_REGION_NAME = "us-east-1"
    AWS_SES_REGION_ENDPOINT = "email.us-east-1.amazonaws.com"


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR("media"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "sample_project.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "sample_project.wsgi.application"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": STATICFILES_DIRS,
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "UPLOADED_FILES_USE_URL": False,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# CSRF TRUSTED ORIGINS (Django 4.0 breaking change)
# Must be configured to work correctly when deployed behind a reverse proxy
# https://docs.djangoproject.com/en/4.0/releases/4.0/#csrf-trusted-origins-changes
# ----------------------------------------------------------------------------

EXTERNAL_DOMAIN = env.str("EXTERNAL_DOMAIN", "localhost")
CSRF_TRUSTED_ORIGINS = [f"https://{EXTERNAL_DOMAIN}", f"http://{EXTERNAL_DOMAIN}"]
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
ALLOWED_CIDR_NETS = env.list(
    "ALLOWED_CIDR_NETS", default=["192.168.0.0/24", "10.0.0.0/8", "172.16.0.0/16"]
)
