"""
(x.v > 5) & (x.v < 3)

(a > 4) & (b < 3)

x.v + y.v

cross-compatible;
"""
from containers.collections.elementary.mappers.base import MapperCollector
from containers.collections.elementary.mappers.callable_mapper \
    import CallableMapper

_operators = ['__add__', ]


def _wrap_dunder_method(name):
    def run_method(x, *args, **kwargs):
        method = getattr(x, name)
        return method(*args, **kwargs)

    return run_method


_operator_dict = {name: _wrap_dunder_method(name) for name in _operators}


class OperatorMapperCreator(object):

    @classmethod
    def build(cls, name, *args, **kwargs):
        operator = _operator_dict[name]
        return CallableMapper(callable_=operator, *args, **kwargs)

    def __add__(self, other):
        pass

# for name, method in _operator_dict.items():
#     setattr(OperatorMapperCreator, name, method)

a = OperatorMapperCreator()

print(OperatorMapperCreator.__dict__['__add__'])
a = a + 2
