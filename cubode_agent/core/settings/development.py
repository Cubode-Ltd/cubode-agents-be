import os
from core.settings.base import *
from core.settings.base import INSTALLED_APPS, MIDDLEWARE, BASE_DIR


DEVELOPMENT = True
DEBUG = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
