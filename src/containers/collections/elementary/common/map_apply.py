from typing import Any

from containers.core.base import MutableMappingBase


class DefaultMapper(object):
    """"""


class EmptyDefault(object):
    """"""


class MissingKeyError(Exception):
    """"""


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


class Collector(object):
    pass


class MapperCollector(Collector):
    """
    collector is independent of types of mapper;
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

    def add_mapper(self, mapper, name=None):
        assert isinstance(mapper, Mapper)
        self._mappers[name] = mapper
        self._collection_size += 1

    def delete_mapper(self, name):
        del self._mappers[name]
        self._collection_size -= 1

    def map_by_mapper(self, name, value):
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

    def map(self, value, names: Any = DefaultMapper):
        """

        :param value: Any
        :param names: refer to above.
        :return:
        """
        names = self._parse_names(names=names)

        if not isinstance(names, list):
            mapped = self.map_by_mapper(name=names, value=value)
        else:
            mapped = dict()
            for name in names:
                mapped[name] = self.map_by_mapper(name=name, value=value)

        return mapped

    def merge(self, other_collector):
        mappers = other_collector.mappers()
        for name, mapper in mappers.items():
            self.add_mapper(mapper=mapper, name=name)


class CollectorLayers(object):

    def __init__(self):
        self._layers = list()

        self.add_layer(index=None)

    @property
    def size(self):
        return len(self._layers)

    def __len__(self):
        return self.size

    def parse_layer_index(self, index=-1, auto_index=True):
        size = self.size

        if (-size) <= index < 0:
            index = size + index
        elif 0 <= index < size:
            pass
        else:
            if auto_index and (index >= size):
                index = size - 1
            else:
                raise IndexError(f"index {index} out of range")

        assert isinstance(index, int)

        return index

    def add_layer(self, index=None):
        collector = MapperCollector()

        if index is not None:
            self._layers.insert(index, collector)
        else:
            self._layers.append(collector)

    def get_layer(self, index):
        return self._layers[index]

    def delete_layer(self, index):
        del self._layers[index]

    def _map_by_layer(self, value, names: Any = DefaultMapper, layer=-1):
        mapper_collector = self._layers[layer]
        return mapper_collector.map(name=names, value=value)

    def map(self, value, names: Any = DefaultMapper, ending_layer=-1):
        ending_layer = self.parse_layer_index(index=ending_layer,
                                              auto_index=False)

        for layer, collector in enumerate(self._layers):
            if layer != ending_layer:
                _names = DefaultMapper
            else:
                _names = names
            value = collector.map(value=value,
                                  names=_names)

            if layer >= ending_layer:
                break

        return value


class MultiLayerMapperCollector(CollectorLayers):

    def add_mapper(self, mapper, name=None, index=-1):
        assert isinstance(mapper, Mapper)

        index = self.parse_layer_index(index=index, auto_index=False)
        collector = self.get_layer(index=index)
        collector.add_mapper(mapper=mapper, name=name)

    def add_layer_and_mapper(self, mapper, name=None):
        self.add_layer(index=None)
        self.add_mapper(mapper=mapper, name=name, index=-1)

    def delete_mapper(self, name=None, index=-1):
        collector = self.get_layer(index=index)
        collector.delete_mapper(name=name)

    def merge(self, other_collector, source_layer=-1, target_layer=-1):
        layer_other_collector = other_collector.get_layer(index=source_layer)
        layer = self.get_layer(index=target_layer)
        layer.merge(other_collector=layer_other_collector)


class CallableMapperCollector(MultiLayerMapperCollector):

    def add(self, mapper, name=None, index=-1, new_layer=False,
            arg_params=None, params=None):

        if not arg_params:
            arg_params = ()

        if not params:
            params = dict()

        if new_layer:
            self.add_layer(index=None)

        mapper = CallableMapper(callable_=mapper, *arg_params, **params)
        self.add_mapper(mapper=mapper, name=name, index=index)

    def decor_add(self, *args, **kwargs):

        def decorator(function):
            self.add(mapper=function, *args, **kwargs)
            return function

        return decorator


class DictMapperCollector(MultiLayerMapperCollector):

    def add(self, mapper, name=None, index=-1, new_layer=False, **kwargs):

        if new_layer:
            self.add_layer(index=None)

        mapper = DictMapper(iterable=mapper, **kwargs)
        self.add_mapper(mapper=mapper, name=name, index=index)


