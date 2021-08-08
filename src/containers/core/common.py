from containers.core.base import Sequence, Set, Mapping


def isinstance_sequence(iterable):
    if isinstance(iterable, Sequence):
        return True
    else:
        return False


def isinstance_mapping(iterable):
    if isinstance(iterable, Mapping):
        return True
    else:
        return False


def isinstance_set(iterable):
    if isinstance(iterable, Set):
        return True
    else:
        return False


def remove_repeat(iterable=()):
    reduced = list()
    for element in iterable:
        if element not in reduced:
            reduced.append(element)
    return reduced
