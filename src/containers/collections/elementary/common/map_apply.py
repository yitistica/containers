from typing import Any

from containers.core.base import MutableMappingBase


class EmptyDefault(object):
    pass


class MissingKeyError(Exception):
    pass


class Mapper(object):

    def map(self, *args, **kwargs):
        return NotImplemented


class CallableMapper(Mapper):
    def __init__(self, callable_, *arg_params, **kwarg_params):
        super().__init__()
        self._mapping = self._parse_mapping(mapping=callable_)
        self._arg_params = arg_params
        self._kwarg_params = kwarg_params

    @staticmethod
    def _parse_mapping(mapping):
        assert callable(mapping)
        return mapping

    def map(self, value):
        """

        :param value: Any, placed 1st.
        :return:
        """
        return self._mapping(value, *self._arg_params, **self._kwarg_params)


class DictMapper(Mapper):
    def __init__(self, iterable, default: Any = EmptyDefault):
        super().__init__()
        self._dict = self._parse_iterable(iterable=iterable)
        self._default = default

    @staticmethod
    def _parse_iterable(iterable):
        dict_ = MutableMappingBase(iterable=iterable)
        return dict_

    def map(self, value):
        try:
            return self._dict[value]
        except KeyError:
            if self._default == EmptyDefault:
                raise MissingKeyError(f"missing key {value} in mapping dict.")
            else:
                return self._default


class MapperCollectorBase(object):
    """
    mapper collection
    """
    def __init__(self):
        self._mappers = dict()
        self._collection_size = 0

    def mappers(self):
        return self._mappers

    @property
    def size(self):
        return self._collection_size

    def names(self):
        return list(self._mappers.keys())

    def _add_mapper(self, mapper, name=None):
        assert isinstance(mapper, Mapper)
        self._mappers[name] = mapper
        self._collection_size += 1

    def delete_mapper(self, name):
        del self._mappers[name]
        self._collection_size -= 1

    def map(self, name, value):
        mapper = self._mappers[name]
        return mapper.map(value)

    def multi_map(self, value, names=None):
        mapped = dict()

        if names is None:
            names = self.names()

        for name in names:
            _mapped = self.map(name=name, value=value)

            if (self.size == 1) & (name is None):
                return _mapped

            mapped[name] = _mapped

        return mapped

    def merge(self, other_collector):
        self._mappers.update(other_collector.mappers())


class CallableMapperCollector(MapperCollectorBase):

    def add(self, mapper, name=None, arg_params=None, params=None):
        if not arg_params:
            arg_params = ()

        if not params:
            params = dict()

        mapper = CallableMapper(callable_=mapper, *arg_params, **params)
        self._add_mapper(mapper=mapper, name=name)

    def decor_add(self, *args, **kwargs):

        def decorator(function):
            self.add(mapper=function, *args, **kwargs)
            return function

        return decorator


class DictMapperCollector(MapperCollectorBase):

    def add(self, mapper, name=None, **kwargs):
        mapper = DictMapper(iterable=mapper, **kwargs)
        self._add_mapper(mapper=mapper, name=name)
