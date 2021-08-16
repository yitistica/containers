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


def isinstance_non_mapping(iterable):
    if isinstance_sequence(iterable=iterable):
        return True
    elif isinstance_set(iterable=iterable):
        return True
    else:
        return False


def remove_repeat(iterable, keep_first=True):
    set_ = set(iterable)

    reduced = list()

    if not keep_first:
        _iter = reversed(iterable)
    else:
        _iter = iterable

    for element in _iter:
        if element in set_:
            reduced.append(element)
            set_.discard(element)

    if not keep_first:
        reduced = reduced[::-1]

    return reduced
