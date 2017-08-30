class BaseBackend(object):
    def __init__(self, key):
        self.key = key

    def get_jwt(self):
        raise NotImplementedError

    def set_jwt(self, token):
        raise NotImplementedError



