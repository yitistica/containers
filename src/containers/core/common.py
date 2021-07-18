

def reduce(iterable=()):
    reduced = list()
    for element in iterable:
        if element not in reduced:
            reduced.append(element)
    return reduced
