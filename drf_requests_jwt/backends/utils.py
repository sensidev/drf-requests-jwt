import urllib
from urllib.parse import urlparse


def build_url(base_url, path, args_dict=None):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse(base_url))
    url_parts[2] = path
    if args_dict is not None:
        url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)
