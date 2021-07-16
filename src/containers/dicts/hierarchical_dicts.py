from collections.abc import MutableMapping
import pandas as pd


d = pd.DataFrame()
d.loc[1]

class LaissezDict(object):
    pass


class AttributeBase(MutableMapping):
    def __init__(self, attributes=()):
        self._attris = dict()
        self.update(attributes)

    @property
    def attris(self):
        return self._attris

    def _get_field(self, field):
        return self._attris[field]

    @property
    def loc(self):
        return None

    def __getitem__(self, field):
        return self._get_field(field=field)

    def _set_field(self, field, value):
        self._attris[field] = value

    def __setitem__(self, field, value):
        self._set_field(field=field, value=value)

    def _delete_field(self, field):
        del self._attris[field]

    def __delitem__(self, field):
        self._delete_field(field=field)

    def __iter__(self):
        return iter(self._attris)

    def __len__(self):
        return len(self._attris)

    def __contains__(self, field):
        return field in self._attris


b = AttributeBase(((1,2), (2, 3)))

b[2,3]