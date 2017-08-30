from drf_requests_jwt.backends.base import BaseBackend


class FileCacheBackend(BaseBackend):
    def __init__(self, key):
        super().__init__(key)

        self.file_path = '/tmp/{key}'.format(key=self.key)

    def get_jwt(self):
        with open(self.file_path, 'r') as f:
            return f.read()

    def set_jwt(self, token):
        with open(self.file_path, 'w') as f:
            f.write(token)
