
from containers.collections.elementary.common.map_apply import CallableMapper, DictMapper, Mappers


class MapperMixin(Mappers):

    def add_dict_mapper(self, name, **kwargs):
        self.add_mapper(name=name, mapper=DictMapper(**kwargs))

    def add_callable_mapper(self, name, **kwargs):
        self.add_mapper(name=name, mapper=CallableMapper(**kwargs))

