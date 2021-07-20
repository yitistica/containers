from containers.core.base import BaseMap


class AttributeBase(BaseMap):
    def __init__(self, attributes=()):
        super().__init__(iterable=attributes)
        self._attris = self._mapping

    @property
    def attris(self):
        return self._attris


class GetAttrMixin(object):
    def __getattr__(self, field):
        return self._get_item(field)


class Attributes(AttributeBase, GetAttrMixin):
    def __init__(self, **attributes):
        AttributeBase.__init__(self, attributes=attributes)


attr = Attributes(a=2, c=4)

print(attr.a)