from containers.core.base import MutableMapping, Sequence, MutableSequence, MutableSet, Set


def reduce(iterable=()):
    reduced = list()
    for element in iterable:
        if element not in reduced:
            reduced.append(element)
    return reduced


def check_if_mapping(iterable):
    if isinstance(iterable, MutableMapping):
        return True
    else:
        return False
