"""
(x.v > 5) & (x.v < 3)

(a > 4) & (b < 3)

x.v + y.v

cross-compatible;
"""

from containers.collections.elementary.mappers.base import Mapper
from containers.collections.elementary.mappers.callable_mapper \
    import CallableMapper


class OperatorMapper(CallableMapper):
    pass


def add(x, other):
    return x + other


def subtract(x, other):
    return x - other


def r_subtract(x, other):
    return other - x


def absolute(x):
    if x < 0:
        x = -x

    return x


def multiply(x, other):
    return x * other


def div(x, other):
    return x / other


def equal(x, other):
    return x == other


def le(x, other):
    return x <= other


def lt(x, other):
    return x < other


def ge(x, other):
    return x >= other


def gt(x, other):
    return x > other


def truediv(x, other):
    return x.__truediv__(other)


class OperatorMapperCreation(object):

    def __init__(self):
        pass

    def __add__(self, other):
        return OperatorMapper(callable_=add, other=other)

    def __radd__(self, other):
        return OperatorMapper(callable_=add, other=other)

    def __sub__(self, other):
        return OperatorMapper(callable_=subtract, other=other)

    def __rsub__(self, other):
        return OperatorMapper(callable_=r_subtract, other=other)

    def __pos__(self):
        return OperatorMapper(callable_=add, other=0)

    def __neg__(self):
        return OperatorMapper(callable_=r_subtract, other=0)

    def __abs__(self):
        return OperatorMapper(callable_=absolute)

    def __mul__(self, other):
        return OperatorMapper(callable_=multiply, other=other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return OperatorMapper(callable_=truediv, other=other)

    def __eq__(self, other):
        return OperatorMapper(callable_=equal, other=other)

    def __le__(self, other):
        return OperatorMapper(callable_=le, other=other)

    def __lt__(self, other):
        return OperatorMapper(callable_=lt, other=other)

    def __ge__(self, other):
        return OperatorMapper(callable_=ge, other=other)

    def __gt__(self, other):
        return OperatorMapper(callable_=gt, other=other)


a = (OperatorMapperCreation() + 3)

print(a)