# -*- coding:utf-8 -*-

from pathlib import Path
from typing import List

## #/definitions/

class DefItem(object):

    def __init__(self):
        self.lookup = None

    @property
    def ref_link(self) -> str:
        return self._ref_link

    @ref_link.setter
    def ref_link(self, value: str):
        self._ref_link = value

    @property
    def ref(self) -> DefItem:
        if self.ref_link and self.lookup:
            return self.lookup.get(self.ref_link)
        return None

    @property
    def description(self) -> str:
        if self._description:
            return self._description
        if self.ref:
            return self.ref.description
        return None

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def type(self) -> str:
        if self._type:
            return self._type
        if self.ref:
            return self.ref.type
        return None

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def required(self) -> List[str]:
        return self._required

    @required.setter
    def required(self, value: List[str]):
        self._required = value

    @property
    def array_item(self) -> DefItem:
        if not self.type == 'array':
            return None
        if self._array_item:
            return self._array_item
        if self.ref:
            return self.ref.array_item
        return None

    @array_item.setter
    def array_item(self, value: DefItem):
        self._array_item = value


# definitions
#     description
#     required
#     properties
#     type
#         string
#         number
#         boolean
#         array
#             items
#         $ref