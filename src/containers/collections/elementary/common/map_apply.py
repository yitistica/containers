from typing import Any

from containers.core.base import MutableMappingBase


class DefaultMapper(object):
    pass


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


class _DictCallable(object):
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
        callable_ = _DictCallable(iterable=iterable, default=default)
        super().__init__(callable_=callable_)


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

    def _parse_names(self, names):
        """
        :param names:
            Cases:
                I. names is not-given (i.e. names = DefaultMapper):
                    1. only 1 mapper:
                        return that mapper's (immutable) name.
                    2. > 1 mappers:
                        return the list of names.
                II. names is given:
                    3. names == None:
                        3.a. None as the name of a mapper, return the name.
                        3.b. no names by None, returns names of all mappers.
                    4. names is an immutable item:
                        return the name.
                    5. names is a list:
                        return the list of names.
        :return: list.
        """
        if names is None:
            if names in self._mappers:
                pass
            else:
                names = self.names()
        elif names == DefaultMapper:
            if self.size == 1:
                names = self.names()[0]
            else:
                names = self.names()
        else:   # either immutable or a list:
            pass

        return names

    def multi_map(self, value, names: Any = DefaultMapper):
        """

        :param value: Any
        :param names: refer to above.
        :return:
        """
        names = self._parse_names(names=names)

        if not isinstance(names, list):
            mapped = self.map(name=names, value=value)
        else:
            mapped = dict()
            for name in names:
                mapped[name] = _mapped = self.map(name=name, value=value)

        return mapped

    def merge(self, other_collector):
        mappers = other_collector.mappers()
        for name, mapper in mappers.items():
            self._add_mapper(mapper=mapper, name=name)


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
