from slugify import slugify


class BaseBackend(object):
    def __init__(self, key):
        self.key = slugify(key)

    def get_jwt(self):
        raise NotImplementedError

    def set_jwt(self, token):
        raise NotImplementedError
