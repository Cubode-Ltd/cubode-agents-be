from core.settings.base import *
from core.settings.base import INSTALLED_APPS, MIDDLEWARE, BASE_DIR


DEVELOPMENT=True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [ BASE_DIR / 'templates' ],
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

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DEBUG = True

# URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'

# The absolute path to the directory where collectstatic will collect static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')

# Additional locations the staticfiles app will traverse
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

