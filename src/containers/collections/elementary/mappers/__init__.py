from typing import Any

from containers.collections.elementary.mappers.base import Mapper, \
    MapperCollector
from containers.collections.elementary.mappers.callable_mapper \
    import CallableMapper
from containers.collections.elementary.mappers.dict_mapper \
    import DictMapper, EmptyDefault


class AddMapperMixinAbstract:

    def __init__(self, collector: MapperCollector):
        self._collector = collector

    @property
    def collector(self):
        return self._collector

    def add(self, *args, **kwargs):
        return NotImplemented

    def add_many(self, *args, **kwargs):
        return NotImplemented


class AddCallableMappersMixin(AddMapperMixinAbstract):

    def add(self, callable_, name=None,
            index=-1, arg_params=None, params=None):

        if not arg_params:
            arg_params = ()

        if not params:
            params = dict()

        mapper = CallableMapper(callable_=callable_, *arg_params, **params)
        self.collector.add_mapper(mapper=mapper, name=name, index=index)

    def add_many(self, *args, params=None, **kwarg_callables):

        if not params:
            params = dict()

        if (len(args) == 1) \
                and (not isinstance(args[0], MapperCollector)) \
                and (len(kwarg_callables) == 0):
            self.add(callable_=args[0], name=None, params=params)
        else:
            for name, arg in enumerate(args):
                if isinstance(arg, MapperCollector):
                    self.collector.merge(other_collector=arg)
                else:
                    self.add(callable_=arg, name=name, params=params)
            for name, callable_ in kwarg_callables.items():
                self.add(callable_=callable_, name=name, params=params)

    def decor_add_mapper(self, *args, **kwargs):

        def wrapped(function):
            self.add(callable_=function, *args, **kwargs)
            return function

        return wrapped


class AddDictMappersMixin(AddMapperMixinAbstract):

    def add(self, iterable, default: Any = EmptyDefault,
            name=None, index=-1):

        mapper = DictMapper(iterable, default=default)

        self.collector.add_mapper(mapper=mapper, name=name, index=index)

    def add_many(self, *args,
                 default: Any = EmptyDefault, **kwarg_iterables):

        if (len(args) == 1) \
                and (not isinstance(args[0], MapperCollector)) \
                and (len(kwarg_iterables) == 0):
            self.add(iterable=args[0], default=default,
                     name=None)
        else:
            for name, arg in enumerate(args):
                if isinstance(arg, MapperCollector):
                    self.collector.merge(other_collector=arg)
                else:
                    self.add(iterable=arg, default=default,
                             name=name)
            for name, iterable in kwarg_iterables.items():
                self.add(iterable=iterable, default=default,
                         name=name)


class MixedMapperCollector(MapperCollector):

    def fix(self, *args, **kwargs):
        return self.callable_mappers.decor_add_mapper(*args, **kwargs)

    @property
    def callable_mappers(self):
        return AddCallableMappersMixin(collector=self)

    @property
    def dict_mappers(self):
        return AddDictMappersMixin(collector=self)
