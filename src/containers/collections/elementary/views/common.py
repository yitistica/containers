"""
Map View:
    1. iterable_view: consists of
        a. .__getitem__(item) method that returns the value of the iterable;
        b. .iterable() property that refers to the original iterable;
        b. .iter_loc(*args, **kwargs) method that generate an iterator of the
        iterable.
    2. map view itself should have __getitem__:


"""
import re
from typing import Any

from containers.collections.elementary.common.map_apply import DefaultMapper, \
    EmptyDefault, \
    DictMapperCollector, CallableMapperCollector


class MapIterView(object):
    def __init__(self, map_view, *args, **kwargs):

        self._map_view = map_view
        self.iter_loc = self._map_view.iterable_view.iter_loc(*args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        location = self.iter_loc.__next__()
        value = self._map_view.iterable[location]
        return location, value, self._map_view.map(id_=location)


class MapViewBase(object):
    def __init__(self, mapper_collector):
        self._iterable_view = None
        self._mappers = mapper_collector

    def set_iterable_view(self, iterable_view):
        self._iterable_view = iterable_view

    @property
    def iterable_view(self):
        if not self._iterable_view:
            raise ValueError('iterable view is not yet set.')

        return self._iterable_view

    @property
    def iterable(self):  # refer to the original iterable
        return self.iterable_view.iterable

    def add(self, *args, **kwargs):
        self._mappers.add(*args, **kwargs)

    def value_map(self, value, names=DefaultMapper, ending_layer=-1):
        mapped = self._mappers.map(value=value, names=names,
                                   ending_layer=ending_layer)
        return mapped

    def map(self, id_, names=DefaultMapper):
        value = self.iterable_view[id_]
        return self.value_map(value=value, names=names)

    @staticmethod
    def _parse_item(item):
        if isinstance(item, int):
            id_, names = item, DefaultMapper
        elif isinstance(item, tuple) and len(item) == 2:
            id_, names = item
        else:
            raise TypeError(f"item {item} cannot be parsed, only int or tuple "
                            f"(sized 2) is accepted.")

        return id_, names

    def __iter__(self):
        return self.iter()

    def __getitem__(self, item):
        id_, names = self._parse_item(item=item)
        return self.map(id_=id_, names=names)

    def iter(self, *args, **kwargs):
        return MapIterView(self, *args, **kwargs)

    @staticmethod
    def _parse_params(**kwargs):
        return kwargs

    def merge_mappers(self, *args, **kwargs):
        self._mappers.merge(*args, **kwargs)


class DictMapView(MapViewBase):
    def __init__(self, *args, default: Any = EmptyDefault, **kwarg_callables):
        super().__init__(mapper_collector=DictMapperCollector())

        if (len(args) == 1) \
                and (not isinstance(args[0], DictMapperCollector)) \
                and (len(kwarg_callables) == 0):
            self.add(mapper=args[0], name=None, default=default)
        else:
            for name, arg in enumerate(args):
                if isinstance(arg, DictMapperCollector):
                    self.merge_mappers(other_collector=arg)
                else:
                    self.add(mapper=arg, name=name, default=default)
            for name, mapper in kwarg_callables.items():
                self.add(mapper=mapper, name=name, default=default)


class CallableMapView(MapViewBase):
    def __init__(self, *args, params=None, **kwarg_callables):
        super().__init__(mapper_collector=CallableMapperCollector())

        if not params:
            params = dict()

        if (len(args) == 1) \
                and (not isinstance(args[0], CallableMapperCollector)) \
                and (len(kwarg_callables) == 0):
            self.add(mapper=args[0], name=None, params=params)
        else:
            for name, arg in enumerate(args):
                if isinstance(arg, CallableMapperCollector):
                    self.merge_mappers(other_collector=arg)
                else:
                    self.add(mapper=arg, name=name, params=params)
            for name, mapper in kwarg_callables.items():
                self.add(mapper=mapper, name=name, params=params)


class RegexView(CallableMapView):
    def __init__(self, patterns, output='both',
                 find_all=False, coerce=True):
        arg_callables, kwarg_callables = \
            self._parse_patterns_into_callable(patterns=patterns)

        params = self._parse_params(output=output,
                                    find_all=find_all,
                                    coerce=coerce)

        super().__init__(*arg_callables, params=params, **kwarg_callables)

    @staticmethod
    def _wrap_find(pattern):

        def _callable(string, output='both', find_all=False, coerce=True):

            if coerce:
                string = str(string)

            results = []
            iterator = re.finditer(pattern, string)
            for match in iterator:
                if output == 'both':
                    result = (match.span(), match.group())
                elif output == 'value':
                    result = match.group()
                elif output == 'span':
                    result = match.span()
                elif output == 'count':
                    result = 1
                else:
                    raise KeyError(f"output {output} can only take both, value or span.")

                if not find_all:
                    return result
                else:
                    results.append(result)

            if output == 'count':
                return len(results)
            else:
                return results

        return _callable

    @staticmethod
    def _parse_patterns_into_callable(patterns):
        arg_callables, kwarg_callables = list(), dict()
        if isinstance(patterns, str):
            arg_callables = [RegexView._wrap_find(patterns)]
        elif isinstance(patterns, (list, tuple)):
            kwarg_callables = dict()
            for pattern in patterns:
                kwarg_callables[pattern] = RegexView._wrap_find(pattern)
        elif isinstance(patterns, dict):
            kwarg_callables = dict()
            for name, pattern in patterns.items():
                kwarg_callables[name] = RegexView._wrap_find(pattern)
        else:
            raise ValueError(f"patterns by type {type(patterns)} is not "
                             f"accepted.")

        return arg_callables, kwarg_callables


class RegexSubView(CallableMapView):
    def __init__(self, pattern, replacement,
                 count=0, flags=0, coerce=True):
        pattern_callable = self._parse_pattern_into_callable(pattern=pattern)
        params = self._parse_params(replacement=replacement, count=count,
                                    flags=flags, coerce=coerce)
        super().__init__(pattern_callable, params=params)

    @staticmethod
    def _wrap_sub(pattern):

        def _callable(string, replacement, count=0, flags=0, coerce=True):

            if coerce:
                string = str(string)

            string = re.sub(pattern=pattern,
                            repl=replacement, string=string, count=count,
                            flags=flags)

            return string

        return _callable

    @staticmethod
    def _parse_pattern_into_callable(pattern):
        if isinstance(pattern, str):
            callable_ = RegexSubView._wrap_sub(pattern)
        else:
            raise ValueError(f"pattern by type {type(pattern)} is not "
                             f"accepted.")

        return callable_


class StrView(object):

    def __init__(self, iterable_view):
        self._iterable_view = iterable_view

    def regex(self, patterns, output='both', find_all=False, coerce=True):
        view = RegexView(patterns=patterns,
                         output=output, find_all=find_all, coerce=coerce)
        view.set_iterable_view(iterable_view=self._iterable_view)
        return view

    def contains(self, patterns):
        view = RegexView(patterns=patterns,
                         output='count', find_all=False, coerce=True)
        view.set_iterable_view(iterable_view=self._iterable_view)
        return view

    def startswith(self, pattern):
        pattern = f"^{pattern}"
        view = RegexView(patterns=pattern,
                         output='count', find_all=False, coerce=True)
        view.set_iterable_view(iterable_view=self._iterable_view)
        return view

    def endswith(self, pattern):
        pattern = f"{pattern}$"
        view = RegexView(patterns=pattern,
                         output='count', find_all=False, coerce=True)
        view.set_iterable_view(iterable_view=self._iterable_view)
        return view

    def sub(self, pattern, replacement, count=0, flags=0, coerce=True):
        view = RegexSubView(pattern=pattern,
                            replacement=replacement, count=count, flags=flags,
                            coerce=coerce)
        view.set_iterable_view(iterable_view=self._iterable_view)
        return view


