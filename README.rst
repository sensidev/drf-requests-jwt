======================================
HTTP Requests with JWT support for DRF
======================================

This is a simple helper used to communicate between Django instances.

It is suited to work well with Django Rest Framework API points and serializers.

Features
--------

- Authenticate with JWT if not already
- Cache JWT with different backends (for now Django Cache and File System)
- Request all pages, before delivering the result
- Deserialize the result with standard DRF serializer classes

Install it
----------

``pip install drf_requests_jwt``

How to use it
-------------

Assuming there is a `devices` paginated API point on another Django instance and you need all devices fetched.

Then you'll inherit from `HttpRequestService` and implement the abstract methods something along these lines:

::

    from apps.devices.models import Device  # Your Device Django model.
    from rest_framework import serializers

    from drf_requests_jwt.services import HttpRequestService


    class DeviceSerializer(serializers.Serializer):
        eui = serializers.CharField()

        def create(self, validated_data):
            return Device(**validated_data)


    class DeviceHttpRequestService(HttpRequestService):
        obtain_jwt_allowed_fail_attempts = 3
        cache_backend_class = 'drf_requests_jwt.backends.django_cache.DjangoCacheBackend'

        def _get_base_url(self):
            return 'https://example.com'

        def _get_jwt_login_url_path(self):
            return 'api/v1/auth/jwt/login/'

        def _get_url_path(self):
            return 'api/v1/devices/'

        def _get_username(self):
            return 'john'

        def _get_password(self):
            return 'snow'

        def _get_params(self):
            return {
                'param1': 'val1',
                'param2': 'val2',
            }

        def get_deserialized_data(self):
            device_list = []

            for device in self.get_results_from_all_pages():
                serializer = DeviceSerializer(data=device)
                if serializer.is_valid():
                    device_list.append(serializer.save())

            return device_list


Now in your business logic where you need the list of devices you'll call it like this:


``devices = DeviceHttpRequestService().get_deserialized_data()``

Mixins
------

There is a mixin helping with deserialization.

::

    from drf_requests_jwt.deserializers import ObjectListDeserializerMixin
    from apps.devices.serializers import DeviceSerializer  # Your device serializer.

    class DeviceDeserializerMixin(ObjectListDeserializerMixin):
        serializer_class = DeviceSerializer

    class DeviceHttpRequestService(DeviceDeserializerMixin, HttpRequestService):
        # ... Other abstract methods implemented

        def get_deserialized_data(self):
            return self.get_deserialized_object_list()

Conclusion
----------

This is quite a specific helper that works well for our use case, but I think it can be easily adjusted to fit other needs.

Please feel free to bring your pull requests. Thanks.