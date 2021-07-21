"""
make attribute decorator like dataclass:
"""

from containers.collections.mixture.attribute.base import AttributeBase
from containers.collections.mixture.attribute.mixins import GetAttrMixin

from dataclasses import dataclass


class Attributes(AttributeBase, GetAttrMixin):
    def __new__(cls, *args, **kwargs):
        return

    def __init__(self, **attributes):
        AttributeBase.__init__(self, attributes=attributes)
