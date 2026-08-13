from .base import *  # noqa: F401,F403
from .base import env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-#m8l@2ara6n)gmz_t*74tuj)=qk#(s*lkn++#(sgeyjci3yj$#",
)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL", default="http://localhost:8000")

STORAGES["staticfiles"]["BACKEND"] = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass
