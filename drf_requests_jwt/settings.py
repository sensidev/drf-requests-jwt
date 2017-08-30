"""
Settings.
"""
import importlib


def import_from_string(val):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        m = importlib.import_module(module_path)
        return getattr(m, class_name)
    except (ImportError, AttributeError) as e:
        msg = 'Could not import {}, {}, {}'.format(val, e.__class__.__name__, e)
        raise ImportError(msg)


DEFAULTS = {
    'OBTAIN_JWT_ALLOWED_FAIL_ATTEMPTS': 3,
    'CACHE_BACKEND_CLASS': 'drf_requests_jwt.backends.file_cache.FileCacheBackend'
}
