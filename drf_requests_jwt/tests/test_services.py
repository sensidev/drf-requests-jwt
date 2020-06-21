from unittest import TestCase

import mock

from drf_requests_jwt.services import HttpRequestService


class BaseHttpRequestServiceTestCase(TestCase):
    def _patch_requests(self):
        patcher = mock.patch('drf_requests_jwt.services.requests')
        self.requests_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def _patch_get_jwt_login_url_path(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_login_url_path')
        self.get_jwt_login_url_path_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def _patch_get_url_path(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_url_path')
        self.get_url_path_mock = patcher.start()
        self.get_url_path_mock.return_value = '/mocked/path/'
        self.addCleanup(patcher.stop)

    def _patch_get_password(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_password')
        self.get_password_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def _patch_get_username(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_username')
        self.get_username_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def _patch_get_base_url(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_base_url')
        self.get_base_url_mock = patcher.start()
        self.get_base_url_mock.return_value = 'http://base:1234'
        self.addCleanup(patcher.stop)

    def _patch_get_headers(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_headers')
        self.get_headers_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def _patch_get_cache_backend(self):
        patcher = mock.patch('drf_requests_jwt.services.HttpRequestService._get_cache_backend')
        self.get_cache_backend_mock = patcher.start()
        self.addCleanup(patcher.stop)


class HttpRequestServiceTestCase(BaseHttpRequestServiceTestCase):
    def setUp(self):
        super().setUp()

        self._patch_requests()
        self._patch_get_cache_backend()
        self._patch_get_headers()
        self._patch_get_base_url()
        self._patch_get_username()
        self._patch_get_password()
        self._patch_get_url_path()
        self._patch_get_jwt_login_url_path()

        self.session_mock = self.requests_mock.Session
        self.get_mock = self.session_mock.return_value.get
        self.post_mock = self.session_mock.return_value.post

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_params')
    def test_init(self, get_params_mock):
        headers_mock = {'h1': 'hv1', 'h2': 'hv2'}
        url_mock = 'mock://host:1234/path/to/resource/'
        params_mock = {'p1': 'pv2', 'p2': 'pv2'}

        self.get_headers_mock.return_value = headers_mock
        self.get_base_url_mock.return_value = 'mock://host:1234'
        self.get_url_path_mock.return_value = 'path/to/resource/'
        get_params_mock.return_value = params_mock

        instance = HttpRequestService(params={'other_param': 'value'})

        self.assertDictEqual(instance.headers, headers_mock)
        self.assertEqual(instance.url, url_mock)
        self.assertDictEqual(instance.params, {'p1': 'pv2', 'p2': 'pv2', 'other_param': 'value'})
        self.assertEqual(instance.session, self.requests_mock.Session.return_value)

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_base_url')
    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_url_path')
    def test_get_url(self, get_url_path_mock, get_base_url_mock):
        get_base_url_mock.return_value = 'http://base:1234'
        get_url_path_mock.return_value = 'path/to/resource/'

        instance = HttpRequestService()
        actual_result = instance._get_url()
        self.assertEqual(actual_result, 'http://base:1234/path/to/resource/')

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_base_url')
    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_url_path')
    def test_get_url_with_trailing_slash(self, get_url_path_mock, get_base_url_mock):
        get_base_url_mock.return_value = 'http://base:1234/'
        get_url_path_mock.return_value = 'path/to/resource/'

        instance = HttpRequestService()
        actual_result = instance._get_url()
        self.assertEqual(actual_result, 'http://base:1234/path/to/resource/')

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_base_url')
    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_login_url_path')
    def test_get_jwt_login_url(self, get_jwt_login_url_path_mock, get_base_url_mock):
        get_base_url_mock.return_value = 'http://base:1234'
        get_jwt_login_url_path_mock.return_value = 'path/to/resource/'

        instance = HttpRequestService()
        actual_result = instance._get_jwt_login_url()
        self.assertEqual(actual_result, 'http://base:1234/path/to/resource/')

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_base_url')
    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_login_url_path')
    def test_get_jwt_login_url_with_trailing_slash(self, get_jwt_login_url_path_mock, get_base_url_mock):
        get_base_url_mock.return_value = 'http://base:1234/'
        get_jwt_login_url_path_mock.return_value = 'path/to/resource/'

        instance = HttpRequestService()
        actual_result = instance._get_jwt_login_url()
        self.assertEqual(actual_result, 'http://base:1234/path/to/resource/')

    def test_get_jwt_cache_key(self):
        self.get_base_url_mock.return_value = 'http://base:1234'
        self.get_username_mock.return_value = 'joe'

        instance = HttpRequestService()
        actual_result = instance._get_jwt_cache_key()
        self.assertEqual(actual_result, 'jwt-http://base:1234-joe')

    def test_get_params(self):
        instance = HttpRequestService()
        self.assertDictEqual(instance._get_params(), {})

    def test_get_results_from_all_pages_successful(self):
        headers_mock = mock.Mock()

        self.get_mock.return_value.status_code = 200
        self.get_mock.return_value.json.side_effect = [
            {'next': 'mock://host1/path1/?offset=2&limit=2', 'results': ['a', 'b']},
            {'next': 'mock://host2/path2/?offset=2&limit=2', 'results': ['x', 'y']},
            {'next': None, 'results': ['h']}
        ]

        self.get_base_url_mock.return_value = 'mock://host0'
        self.get_url_path_mock.return_value = 'path0/'
        params_mock = {'param1': ['1'], 'param2': ['2']}

        instance = HttpRequestService(params=params_mock)

        instance.headers = headers_mock

        actual_result = instance.get_results_from_all_pages()

        self.assertListEqual(actual_result, ['a', 'b', 'x', 'y', 'h'])

        self.get_mock.assert_any_call('mock://host0/path0/', headers=headers_mock, params=params_mock)
        params_mock.update({'offset': ['2'], 'limit': ['2']})

        self.get_mock.assert_any_call('mock://host1/path1/', headers=headers_mock, params=params_mock)
        self.get_mock.assert_any_call('mock://host2/path2/', headers=headers_mock, params=params_mock)

        self.assertEqual(self.get_mock.call_count, 3)

    @mock.patch('drf_requests_jwt.services.HttpRequestService._should_update_authorization_header')
    @mock.patch('drf_requests_jwt.services.HttpRequestService.update_authorization_header')
    def test_get_results_from_all_pages_unauthorized_should_update_header(self, update_mock, should_update_mock):
        should_update_mock.side_effect = [True, False]

        headers_mock = mock.Mock()
        params_mock = mock.Mock()

        self.get_mock.return_value.status_code = 401

        self.get_base_url_mock.return_value = 'mock://host0'
        self.get_url_path_mock.return_value = 'path0/'

        instance = HttpRequestService()

        instance.headers = headers_mock
        instance.params = params_mock

        actual_result = instance.get_results_from_all_pages()

        self.assertListEqual(actual_result, [])

        self.get_mock.assert_any_call('mock://host0/path0/', headers=headers_mock, params=params_mock)
        self.assertEqual(self.get_mock.call_count, 2)
        self.assertEqual(should_update_mock.call_count, 2)
        update_mock.assert_called_once_with()

    @mock.patch('drf_requests_jwt.services.HttpRequestService._should_update_authorization_header')
    @mock.patch('drf_requests_jwt.services.HttpRequestService.update_authorization_header')
    def test_get_results_from_all_pages_unauthorized_should_not_update_header(self, update_mock, should_update_mock):
        should_update_mock.return_value = False

        headers_mock = mock.Mock()
        params_mock = mock.Mock()

        self.get_mock.return_value.status_code = 401

        self.get_base_url_mock.return_value = 'mock://host0'
        self.get_url_path_mock.return_value = 'path0/'

        instance = HttpRequestService()

        instance.headers = headers_mock
        instance.params = params_mock

        actual_result = instance.get_results_from_all_pages()

        self.assertListEqual(actual_result, [])

        self.get_mock.assert_called_once_with('mock://host0/path0/', headers=headers_mock, params=params_mock)
        should_update_mock.assert_called_once_with()
        self.assertEqual(update_mock.call_count, 0)

    def test_get_results_from_all_pages_error(self):
        headers_mock = mock.Mock()
        params_mock = mock.Mock()

        self.get_mock.return_value.status_code = 404

        self.get_base_url_mock.return_value = 'mock://host0'
        self.get_url_path_mock.return_value = 'path0/'

        instance = HttpRequestService()

        instance.headers = headers_mock
        instance.params = params_mock

        self.assertRaises(Exception, instance.get_results_from_all_pages)

        self.get_mock.assert_called_once_with('mock://host0/path0/', headers=headers_mock, params=params_mock)

    def test_should_update_authorization_header_true(self):
        instance = HttpRequestService()

        instance.obtain_jwt_fail_attempts = 2
        instance.obtain_jwt_allowed_fail_attempts = 3

        self.assertTrue(instance._should_update_authorization_header())

        instance.obtain_jwt_fail_attempts = 3
        instance.obtain_jwt_allowed_fail_attempts = 3

        self.assertTrue(instance._should_update_authorization_header())

    def test_should_update_authorization_header_false(self):
        instance = HttpRequestService()

        instance.obtain_jwt_fail_attempts = 4
        instance.obtain_jwt_allowed_fail_attempts = 3

        self.assertFalse(instance._should_update_authorization_header())

    def test_set_jwt_token_to_cache(self):
        instance = HttpRequestService()
        instance._set_jwt_token_to_cache('token123')

        self.get_cache_backend_mock.return_value.set_jwt.assert_called_once_with('token123')

    def test_get_jwt_token_from_cache(self):
        expected_result = mock.Mock()
        self.get_cache_backend_mock.return_value.get_jwt.return_value = expected_result

        instance = HttpRequestService()

        actual_result = instance._get_jwt_token_from_cache()

        self.assertEqual(actual_result, expected_result)

        self.get_cache_backend_mock.return_value.get_jwt.assert_called_once_with()

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_token')
    def test_update_authorization_header(self, get_jwt_token_mock):
        get_jwt_token_mock.return_value = 'updated-token12345'

        self.get_headers_mock.return_value = {}

        instance = HttpRequestService()

        instance.update_authorization_header()

        self.assertEqual(instance.headers['Authorization'], 'Bearer updated-token12345')

    @mock.patch('drf_requests_jwt.services.HttpRequestService._set_jwt_token_to_cache')
    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_login_url')
    def test_get_jwt_token_success(self, get_jwt_login_url_mock, set_jwt_token_to_cache_mock):
        self.post_mock.return_value.status_code = 200
        self.post_mock.return_value.json.return_value = {'access': 'the-token12345', 'refresh': 'the-refresh-token122'}

        get_jwt_login_url_mock.return_value = 'mock://host0:1234/path/to/jwt/login/'

        instance = HttpRequestService()

        actual_result = instance._get_jwt_token()

        self.assertEqual(actual_result, 'the-token12345')

        self.post_mock.assert_called_once_with('mock://host0:1234/path/to/jwt/login/', data={
            'username': self.get_username_mock.return_value,
            'password': self.get_password_mock.return_value,
        })

        set_jwt_token_to_cache_mock.assert_called_once_with('the-token12345')

    @mock.patch('drf_requests_jwt.services.HttpRequestService._set_jwt_token_to_cache')
    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_login_url')
    def test_get_jwt_token_fail(self, get_jwt_login_url_mock, set_jwt_token_to_cache_mock):
        self.post_mock.return_value.status_code = 400
        self.post_mock.return_value.json.return_value = {'token': 'the-token12345', 'refresh': 'the-refresh-token122'}

        get_jwt_login_url_mock.return_value = 'mock://host0:1234/path/to/jwt/login/'

        instance = HttpRequestService()

        self.assertRaises(Exception, instance._get_jwt_token)

        self.post_mock.assert_called_once_with('mock://host0:1234/path/to/jwt/login/', data={
            'username': self.get_username_mock.return_value,
            'password': self.get_password_mock.return_value,
        })

        self.assertEqual(set_jwt_token_to_cache_mock.call_count, 0)


class HttpRequestHeadersTestCase(BaseHttpRequestServiceTestCase):
    def setUp(self):
        self._patch_get_base_url()
        self._patch_get_base_url()
        self._patch_get_username()
        self._patch_get_password()
        self._patch_get_url_path()

    @mock.patch('drf_requests_jwt.services.HttpRequestService._get_jwt_token_from_cache')
    def test_get_headers(self, get_jwt_token_from_cache_mock):
        get_jwt_token_from_cache_mock.return_value = 'jwt-username-token123456'
        instance = HttpRequestService()
        self.assertDictEqual(instance._get_headers(), {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer jwt-username-token123456'
        })
