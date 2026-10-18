import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-change-me-in-production-9f2k1m4x7q0z",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# ---------------------------------------------------------------------------
# ALLOWED_HOSTS
# ---------------------------------------------------------------------------
# In production (DEBUG=False), the DJANGO_ALLOWED_HOSTS environment variable
# must contain a comma-separated list of valid hostnames.
#
# In development (DEBUG=True), localhost variants are always appended so
# that local testing never fails with a 400 Bad Request.
#
# As a safety net for the first Runko/Runsite deployment (before you've
# confirmed the app's temporary URL), a wildcard "*" is added ONLY when
# DJANGO_ALLOWED_HOSTS is empty AND DEBUG is False. This is a temporary
# convenience — once you know the app URL, set DJANGO_ALLOWED_HOSTS to
# that value (comma-separated) and remove this fallback.
# ---------------------------------------------------------------------------

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if h.strip()
]

if DEBUG:
    for host in ("localhost", "127.0.0.1", "[::1]", "0.0.0.0"):
        if host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)
elif not ALLOWED_HOSTS:
    # Temporary fallback for the first deployment — replace via env var ASAP.
    ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "betty_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_profile",
                "core.context_processors.studio_context",
            ],
        },
    },
]

WSGI_APPLICATION = "betty_portfolio.wsgi.application"

# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------
# If DATABASE_URL is set (as it will be on Runsite, Railway, Render, etc.),
# Django connects to that PostgreSQL instance.
# If DATABASE_URL is missing (local development), it falls back to SQLite.
# ---------------------------------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# ---------------------------------------------------------------------------
# CLOUDINARY MEDIA STORAGE
# ---------------------------------------------------------------------------
# These values are read from environment variables. On Runsite, set them
# in the dashboard's Environment Variables section.
#
# Locally, put them in .env:
#   CLOUDINARY_CLOUD_NAME=dvkujw253
#   CLOUDINARY_API_KEY=746253755269137
#   CLOUDINARY_API_SECRET=<your real secret>
# ---------------------------------------------------------------------------

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY", ""),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", ""),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/studio/login/"
LOGIN_REDIRECT_URL = "/studio/"
LOGOUT_REDIRECT_URL = "/"