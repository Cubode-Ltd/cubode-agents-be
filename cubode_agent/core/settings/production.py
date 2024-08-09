import os
from core.settings.base import *
from core.settings.base import BASE_DIR

DEBUG = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / 'assets' / 'html',
            BASE_DIR / 'assets' / 'templates',
        ],
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

# AWS S3 configurations
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")

AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False

AWS_LOCATION = os.environ.get("AWS_LOCATION", "static")
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_EXPIRE = 300

# CLOUD FRONT
AWS_DEFAULT_ACL = None
AWS_S3_CLOUDFRONT_DOMAIN = os.environ.get("AWS_S3_CLOUDFRONT_DOMAIN", "")
AWS_S3_CUSTOM_DOMAIN = AWS_S3_CLOUDFRONT_DOMAIN + '/' + AWS_STORAGE_BUCKET_NAME
AWS_CLOUDFRONT_KEY_ID = os.environ.get("AWS_CLOUDFRONT_KEY_ID", "").strip()
AWS_CLOUDFRONT_KEY = os.environ.get("AWS_CLOUDFRONT_KEY", "").replace("\\n", "\n").encode('ascii').strip()

# Static files (CSS, JavaScript, Images)
STATIC_LOCATION = "static"
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files
PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
