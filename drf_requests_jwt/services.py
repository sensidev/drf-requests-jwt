"""
Services.
"""
import logging
import requests
from urllib.parse import urlparse, parse_qs

from drf_requests_jwt import settings
from drf_requests_jwt.backends.utils import build_url

logger = logging.getLogger(__name__)


class HttpRequestService(object):
    obtain_jwt_allowed_fail_attempts = settings.DEFAULTS.get('OBTAIN_JWT_ALLOWED_FAIL_ATTEMPTS')
    cache_backend_class = settings.DEFAULTS.get('CACHE_BACKEND_CLASS')

    def __init__(self, params=None):
        super().__init__()

        self.cache_backend = self._get_cache_backend()

        self.params = params or {}
        self.params.update(self._get_params())

        self.headers = self._get_headers()
        self.url = self._get_url()

        self.session = requests.Session()

        self.obtain_jwt_fail_attempts = 0

    def _get_cache_backend(self):
        resolved_backend_class = settings.import_from_string(self.cache_backend_class)
        return resolved_backend_class(self._get_jwt_cache_key())

    def _get_base_url(self):
        raise NotImplementedError

    def _get_url_path(self):
        raise NotImplementedError

    def _get_url(self):
        return build_url(base_url=self._get_base_url(), path=self._get_url_path())

    def _get_jwt_login_url_path(self):
        raise NotImplementedError

    def _get_jwt_login_url(self):
        return build_url(base_url=self._get_base_url(), path=self._get_jwt_login_url_path())

    def _get_username(self):
        raise NotImplementedError

    def _get_password(self):
        raise NotImplementedError

    def _get_params(self):
        return {}

    def _get_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=self._get_jwt_token_from_cache())
        }

    def get_results_from_all_pages(self):
        next_url = self.url
        result_list = []

        while True:
            url_parse = urlparse(next_url)

            self.params.update(parse_qs(url_parse.query))

            next_url = '{scheme}://{netloc}{path}'.format(
                scheme=url_parse.scheme, netloc=url_parse.netloc, path=url_parse.path
            )

            response = self.session.get(next_url, headers=self.headers, params=self.params)

            logger.debug('Request url: {} with params {}'.format(next_url, self.params))

            if response.status_code == 200:
                response_json = response.json()
                next_url = response_json.get('next')
                result_list.extend(response_json.get('results', []))
            elif response.status_code == 401:
                if self._should_update_authorization_header():
                    self.update_authorization_header()
                else:
                    break
            else:
                raise Exception('Wrong response status code: {code}, content: {content}'.format(
                    code=response.status_code,
                    content=response.content
                ))

            if not bool(next_url):
                break

        return result_list

    def write_results_from_all_pages_to_file(self, filename):
        results = self.get_results_from_all_pages()

        with open(filename, 'w') as output:
            json.dump(results, output)

    def update_authorization_header(self):
        token = self._get_jwt_token()
        self.headers['Authorization'] = 'Bearer {token}'.format(token=token)

    def get_deserialized_data(self):
        raise NotImplementedError

    def _get_jwt_token(self):
        payload = {
            'username': self._get_username(),
            'password': self._get_password()
        }
        url = self._get_jwt_login_url()
        logger.debug('Request url: {}'.format(url))
        response = self.session.post(url, data=payload)

        if response.status_code == 200:
            response_dict = response.json()
            token = response_dict.get('access')
            self._set_jwt_token_to_cache(token)
            logger.debug('Received a fresh JWT token')
            return token
        else:
            self.obtain_jwt_fail_attempts += 1
            logger.warning('Attempt to get a JWT token failed')
            raise Exception('Wrong response status code: {code}, content: {content}'.format(
                code=response.status_code,
                content=response.content
            ))

    def _should_update_authorization_header(self):
        return self.obtain_jwt_fail_attempts <= self.obtain_jwt_allowed_fail_attempts

    def _set_jwt_token_to_cache(self, token):
        self.cache_backend.set_jwt(token)

    def _get_jwt_token_from_cache(self):
        return self.cache_backend.get_jwt()

    def _get_jwt_cache_key(self):
        return 'jwt-{url}-{username}'.format(url=self._get_base_url(), username=self._get_username())
