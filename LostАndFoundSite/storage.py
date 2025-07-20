import hashlib

from django.conf import settings
from django.core.cache import cache
from storages.backends.s3 import S3Storage

class CachedS3Storage(S3Storage):
    """ adds caching for temporary urls """

    def url(self, name):
        # Add a prefix to avoid conflicts with any other apps
        key = hashlib.md5(f"CachedS3Boto3Storage_{name}".encode()).hexdigest()
        result = cache.get(key)
        if result:
            return result

        # No cached value exists, follow the usual logic
        result = super().url(name)

        # Cache the result for 3/4 of the temp_url's lifetime.
        timeout = self.querystring_expire
        timeout = int(timeout*.75)
        cache.set(key, result, timeout)

        return result