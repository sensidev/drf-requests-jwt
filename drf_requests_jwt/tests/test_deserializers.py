from unittest import TestCase

import mock

from drf_requests_jwt.deserializers import ObjectListDeserializerMixin


class ObjectListDeserializerMixinTestCase(TestCase):
    def test_get_deserialized_object_list_raise_exception(self):
        instance = ObjectListDeserializerMixin()
        self.assertRaises(Exception, instance.get_deserialized_object_list)

    def test_get_deserialized_object_list_all_valid(self):
        instance = ObjectListDeserializerMixin()
        instance.get_results_from_all_pages = mock.Mock(return_value=[{'k': 'o1'}, {'k': 'o2'}, {'k': 'o3'}])
        instance.serializer_class = mock.Mock()

        object1 = mock.Mock()
        object2 = mock.Mock()
        object3 = mock.Mock()

        serializer1 = mock.Mock(is_valid=mock.Mock(return_value=True), save=mock.Mock(return_value=object1))
        serializer2 = mock.Mock(is_valid=mock.Mock(return_value=True), save=mock.Mock(return_value=object2))
        serializer3 = mock.Mock(is_valid=mock.Mock(return_value=True), save=mock.Mock(return_value=object3))

        instance.serializer_class.side_effect = [serializer1, serializer2, serializer3]

        actual_result = instance.get_deserialized_object_list()

        self.assertListEqual(actual_result, [object1, object2, object3])

        instance.get_results_from_all_pages.assert_called_once_with()

        instance.serializer_class.assert_any_call(data={'k': 'o1'})
        instance.serializer_class.assert_any_call(data={'k': 'o2'})
        instance.serializer_class.assert_any_call(data={'k': 'o3'})

        self.assertEqual(instance.serializer_class.call_count, 3)

    def test_get_deserialized_object_list_one_invalid(self):
        instance = ObjectListDeserializerMixin()
        instance.get_results_from_all_pages = mock.Mock(return_value=[{'k': 'o1'}, {'k': 'o2'}, {'k': 'o3'}])
        instance.serializer_class = mock.Mock()

        object1 = mock.Mock()
        object2 = mock.Mock()
        object3 = mock.Mock()

        serializer1 = mock.Mock(is_valid=mock.Mock(return_value=True), save=mock.Mock(return_value=object1))
        serializer2 = mock.Mock(is_valid=mock.Mock(return_value=False), save=mock.Mock(return_value=object2))
        serializer3 = mock.Mock(is_valid=mock.Mock(return_value=True), save=mock.Mock(return_value=object3))

        instance.serializer_class.side_effect = [serializer1, serializer2, serializer3]

        actual_result = instance.get_deserialized_object_list()

        self.assertListEqual(actual_result, [object1, object3])

        instance.get_results_from_all_pages.assert_called_once_with()

        instance.serializer_class.assert_any_call(data={'k': 'o1'})
        instance.serializer_class.assert_any_call(data={'k': 'o2'})
        instance.serializer_class.assert_any_call(data={'k': 'o3'})

        self.assertEqual(instance.serializer_class.call_count, 3)
