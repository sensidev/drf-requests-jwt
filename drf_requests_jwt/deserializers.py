"""
Deserializers.
"""
import logging

logger = logging.getLogger(__name__)


class ObjectListDeserializerMixin(object):
    serializer_class = None

    def get_deserialized_object_list(self):
        object_list = []

        if self.serializer_class is None:
            raise Exception('`serializer_class` is required')

        for object_json in self.get_results_from_all_pages():
            logger.debug("Serializing {}".format(object_json))
            serializer = self.serializer_class(data=object_json)
            if serializer.is_valid():
                object_list.append(serializer.save())
            else:
                logger.warning("Serializer has errors {}".format(serializer.errors))

        return object_list
