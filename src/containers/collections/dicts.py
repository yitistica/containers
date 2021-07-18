from containers.core.base import BaseMap, BaseSequence




class OrderedDict(BaseMap):
    def __init__(self, items=()):
        self._key_order = list()
        super().__init__(items=items)

    def _get_item(self, key):
        return self._mapping[key]

    def _set_item(self, key, value):
        self._mapping[key] = value

    def _delete_item(self, key):
        del self._mapping[key]



class BaseDict(object):
    def __init__(self, *items):
        for item in items:
            key, value = item.key, item.value


class TemplateDict(object):
    def __init__(self):
        pass



class TreeDict(object):

    def __init__(self):
        pass



class LaissezDict(object):
    def __init__(self, items):
        pass

