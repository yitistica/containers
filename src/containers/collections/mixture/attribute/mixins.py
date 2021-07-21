
class GetAttrMixin(object):
    def __getattr__(self, field):
        return self._get_item(field)


class ObjectAttributeOccupiedError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is already used as an attribute of the object.'
        super().__init__(message)


class ImmutableFieldError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is not mutable after instantiation.'
        super().__init__(message)


class FieldNotExistError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field <{field}> does not exist.'
        super().__init__(message)


class NullFieldError(Exception):  # TEMP
    def __init__(self, field, value):
        message = f'field <{field}> is a null value (<{value}>).'
        super().__init__(message)


class ImmutableFieldMixin(object):
    def __init__(self, fields):
        self._immutable_fields = fields

    @property
    def immutable_fields(self):
        return self._immutable_fields

    def _check_immutable(self, field):
        if (field in self._immutable_fields) and (field in self.attrs):
            raise ImmutableFieldError(field)


class NotNullFieldMixin(object):
    def __init__(self, fields):
        if not fields:
            fields = list()
        self._not_null_fields = fields

    def _check_exist(self, field):
        if not ((field in self._not_null_fields) and (field in self.attrs)):
            raise FieldNotExistError(field)

    def _check_null(self, field, null_forms=None):
        self._check_exist(field=field)

        if (not null_forms) and isinstance(null_forms, (list, set, tuple)):
            raise TypeError(f"null forms <{null_forms}> is empty or not a list, set or tuple.")

        value = self.attrs.get(field)
        if value in null_forms:
            raise NullFieldError(field=field, value=value)
