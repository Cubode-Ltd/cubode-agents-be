from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = None

class CSSStorage(S3Boto3Storage):
    location = 'css' # location = os.path.join(settings.BASE_DIR, 'static/css')
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = None


class CSSFileStorage(FileSystemStorage):
    """
    Custom storage backend for storing CSS files locally.
    """
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATIC_ROOT / 'css'
        super().__init__(*args, **kwargs)