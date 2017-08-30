"""
Deserializers.
"""


class ObjectListDeserializerMixin(object):
    serializer_class = None

    def get_deserialized_object_list(self):
        object_list = []

        if self.serializer_class is None:
            raise Exception('`serializer_class` is required')

        for object_json in self.get_results_from_all_pages():
            serializer = self.serializer_class(data=object_json)
            if serializer.is_valid():
                object_list.append(serializer.save())

        return object_list
