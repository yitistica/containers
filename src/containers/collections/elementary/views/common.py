"""
Map View:
    1. iterable_view: consists of
        a. .__getitem__(item) method that returns the value of the iterable;
        b. .iterable() property that refers to the original iterable;
        b. .iter_loc(*args, **kwargs) method that generate an iterator of the iterable.
    2. map view itself should have __getitem__:
"""
import re
from typing import Any

from containers.collections.elementary.common.map_apply import EmptyDefault, DictMapperCollector, \
    CallableMapperCollector


class MapIterView(object):
    def __init__(self, map_view, *args, **kwargs):

        self._map_view = map_view
        self.iter_loc = self._map_view.iterable_view.iter_loc(*args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        location = self.iter_loc.__next__()
        value = self._map_view.iterable[location]
        return location, value, self._map_view[location]


class MapViewBase(object):
    def __init__(self, iterable_view, mapper_collector):
        self._iterable_view = iterable_view
        self._mappers = mapper_collector

    @property
    def iterable_view(self):
        return self._iterable_view

    @property
    def iterable(self):  # refer to the original iterable
        return self._iterable_view.iterable

    def add(self, mapper, name=None, *args, **kwargs):
        self._mappers.add(mapper=mapper, name=name, *args, **kwargs)

    def value_map(self, value, names=None):

        if names is None:
            pass
        elif not isinstance(names, (set, list)):
            return self._mappers.map(name=names, value=value)

        mapped = self._mappers.multi_map(names=names, value=value)

        return mapped

    def map(self, id_, names=None):
        value = self._iterable_view[id_]
        return self.value_map(value=value, names=names)

    @staticmethod
    def _parse_item(item):
        if isinstance(item, int):
            id_, names = item, None
        elif isinstance(item, tuple):  # mappers;
            id_, names = item
        else:
            raise TypeError(f"item {item} cannot be parsed, only int or tuple (sized 2) is accepted.")

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

    def merge_mappers(self, other_collector):
        self._mappers.merge(other_collector=other_collector)


class DictMapView(MapViewBase):
    def __init__(self, iterable_view, *args, default: Any = EmptyDefault, **kwarg_callables):
        super().__init__(iterable_view=iterable_view, mapper_collector=DictMapperCollector())

        if (len(args) == 1) and (not isinstance(args[0], DictMapperCollector)) and (len(kwarg_callables) == 0):
            self.add(mapper=args[0], name=None, default=default)
        else:
            for name, arg in enumerate(args):
                if isinstance(arg, CallableMapperCollector):
                    self.merge_mappers(other_collector=arg)
                else:
                    self.add(mapper=arg, name=name, default=default)
            for name, mapper in kwarg_callables.items():
                self.add(mapper=mapper, name=name, default=default)


class CallableMapView(MapViewBase):
    def __init__(self, iterable_view, *args, params=None, **kwarg_callables):
        super().__init__(iterable_view=iterable_view, mapper_collector=CallableMapperCollector())

        if not params:
            params = dict()

        if (len(args) == 1) and (not isinstance(args[0], CallableMapperCollector)) and (len(kwarg_callables) == 0):
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
    def __init__(self, iterable_view, patterns, output='both', find_all=False, coerce=True):
        arg_callables, kwarg_callables = self._parse_patterns_into_callable(patterns=patterns)
        params = self._parse_params(output=output, find_all=find_all, coerce=coerce)
        super().__init__(iterable_view, *arg_callables, params=params, **kwarg_callables)

    @staticmethod
    def _wrap_find(pattern):

        def _callabe(string, output='both', find_all=False, coerce=True):

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

        return _callabe

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
            raise ValueError(f"patterns by type {type(patterns)} is not accepted.")

        return arg_callables, kwarg_callables


class RegexSubView(CallableMapView):
    def __init__(self, iterable_view, pattern, replacement, count=0, flags=0, coerce=True):
        pattern_callabe = self._parse_pattern_into_callable(pattern=pattern)
        params = self._parse_params(replacement=replacement, count=count, flags=flags, coerce=coerce)
        super().__init__(iterable_view, pattern_callabe, params=params)

    @staticmethod
    def _wrap_sub(pattern):

        def _callabe(string, replacement, count=0, flags=0, coerce=True):

            if coerce:
                string = str(string)

            string = re.sub(pattern=pattern, repl=replacement, string=string, count=count, flags=flags)

            return string

        return _callabe

    @staticmethod
    def _parse_pattern_into_callable(pattern):
        if isinstance(pattern, str):
            callable_ = RegexSubView._wrap_sub(pattern)
        else:
            raise ValueError(f"pattern by type {type(pattern)} is not accepted.")

        return callable_


class StrView(object):

    def __init__(self, iterable_view):
        self._iterable_view = iterable_view

    def regex(self, patterns, output='both', find_all=False, coerce=True):
        return RegexView(iterable_view=self._iterable_view,
                         patterns=patterns, output=output, find_all=find_all, coerce=coerce)

    def contains(self, patterns):
        regex_view = RegexView(iterable_view=self._iterable_view,
                               patterns=patterns, output='count', find_all=False, coerce=True)
        return regex_view

    def startswith(self, pattern):
        pattern = f"^{pattern}"
        regex_view = RegexView(iterable_view=self._iterable_view,
                               patterns=pattern, output='count', find_all=False, coerce=True)
        return regex_view

    def endswith(self, pattern):
        pattern = f"{pattern}$"
        regex_view = RegexView(iterable_view=self._iterable_view,
                               patterns=pattern, output='count', find_all=False, coerce=True)
        return regex_view

    def sub(self, pattern, replacement, count=0, flags=0, coerce=True):
        sub_view = RegexSubView(iterable_view=self._iterable_view,
                                pattern=pattern, replacement=replacement, count=count, flags=flags, coerce=coerce)
        return sub_view



class ContainView(CallableMapView):
    """rely on bool view;
     compare with another iterable;

     """
    def __init__(self, iterable_view):
        self._iterable_view = iterable_view