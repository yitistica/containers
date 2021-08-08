from typing import Any

from containers.core.base import MutableMappingBase


class EmptyDefault(object):
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


class _CallableDict(MutableMappingBase):
    def __init__(self, iterable=(), default: Any = EmptyDefault):
        super().__init__(iterable=iterable)
        self._default = default

    def __call__(self, value):
        try:
            return self._mapping[value]
        except KeyError as e:
            if self._default == EmptyDefault:
                raise e
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
        return mapper(value)

    def multi_map(self, names, value):
        mapped = dict()
        for name in names:
            mapped[name] = self.map(name=name, value=value)

        return mapped
