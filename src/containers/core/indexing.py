"""

default __getitems__


keys.filter(*args, **kwargs) without callable;

if isinstance(kwarg, str), then check key;
keys.order_by()
values.


keeping track of true index for key and value;
"""

class _BaseIndexer(object):
    def _get_item(self, key):
        pass

    def __getitem__(self, key):
        return self._get_item(key=key)

