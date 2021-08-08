from typing import Any

from containers.core.base import MutableMappingBase


class EmptyDefault(object):
    pass


class MissingKeyError(Exception):
    pass


class Mapper(object):
    pass


class CallableMapper(Mapper):
    def __init__(self, callable_, **kwargs):
        super().__init__()
        self._mapping = self._parse_mapping(mapping=callable_)
        self._params = kwargs

    @staticmethod
    def _parse_mapping(mapping):
        assert callable(mapping)
        return mapping

    def map(self, value):
        return self._mapping(value, **self._params)


class _CallableDict(object):
    def __init__(self, iterable=(), default: Any = EmptyDefault):
        self._dict = MutableMappingBase(iterable=iterable)
        self._default = default

    def __call__(self, value):
        try:
            return self._dict[value]
        except KeyError as e:
            if self._default == EmptyDefault:
                raise MissingKeyError(f"missing key {value} in mapping dict.")
            else:
                return self._default


class DictMapper(CallableMapper):
    def __init__(self, iterable, default: Any = EmptyDefault):
        callable_ = self._convert_dict_to_callable(iterable=iterable, default=default)
        super().__init__(callable_=callable_)

    @staticmethod
    def _convert_dict_to_callable(iterable, default):
        callable_dict = _CallableDict(iterable=iterable, default=default)
        return callable_dict


class Mappers(object):
    """
    mapper collection
    """
    def __init__(self):
        self._mapper = dict()

    def add_mapper(self, name, mapper):
        assert isinstance(mapper, Mapper)
        self._mapper[name] = mapper

    def delete_mapper(self, name):
        del self._mapper[name]

    def map(self, name, value):
        mapper = self._mapper[name]
        return mapper.map(value)

    def multi_map(self, value, names=None, return_first=False):
        mapped = dict()

        if not names:
            names = list(self._mapper.keys())

        for name in names:
            if return_first:
                return self.map(name=name, value=value)
            else:
                mapped[name] = self.map(name=name, value=value)

        return mapped