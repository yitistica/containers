from typing import Any

from containers.core.base import MutableMappingBase
from containers.collections.elementary.mappers.callable_mapper \
    import CallableMapper


class EmptyDefault(object):
    pass


class MissingKeyError(Exception):
    pass


class CallableDict(object):
    def __init__(self, iterable, default: Any = EmptyDefault):
        self._dict = self._parse_iterable(iterable=iterable)
        self._default = None
        self.set_default(default=default)

    def set_default(self, default):
        self._default = default

    @staticmethod
    def _parse_iterable(iterable):
        dict_ = MutableMappingBase(iterable=iterable)
        return dict_

    def __getitem__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            if self._default == EmptyDefault:
                raise MissingKeyError(f"missing key {item} in mapping dict.")
            else:
                return self._default

    def __call__(self, item):
        return self[item]


class DictMapper(CallableMapper):
    def __init__(self, iterable, default: Any = EmptyDefault):
        callable_ = CallableDict(iterable=iterable, default=default)
        super().__init__(callable_=callable_)

