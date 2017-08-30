from django.core.cache import cache

from drf_requests_jwt.backends.base import BaseBackend


class DjangoCacheBackend(BaseBackend):
    def get_jwt(self):
        return cache.get(self.key)

    def set_jwt(self, token):
        cache.set(self.key, token)
