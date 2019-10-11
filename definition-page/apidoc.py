# -*- coding:utf-8 -*-

# https://stackoverflow.com/questions/15853469/putting-current-class-as-return-type-annotation
from __future__ import annotations

import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import List, Dict, Optional
from resource import Resources

logger = logging.getLogger("data.apidoc")

class ApiDoc(object):

    def __init__(self, version):
        self._storage = {}
        self._version = version
        self._resouces = Resources(version)
        self._load_doc(version)

    @property
    def storage(self) -> Dict[str, DefItem]:
        return self._storage

    @property
    def resources(self) -> Resources:
        return self._resouces

    def fetch(self, key) -> Optional[DefItem]:
        return self.storage.get(key)

    def store(self, key, value: DefItem):
        self.storage[key] = value

    def search(self, path: str) -> Optional[DefItem]:
        root = path.split('.')[0]
        root_key = self.find_root_key(root)
        if not root_key:
            return None
        print('root_key of {} is {}'.format(path, root_key))

        root_item = self.fetch(root_key)

        parts = path.split('.', maxsplit=1)
        if len(parts) == 1:
            return root_item

        return root_item.search(parts[1])

    def find_root_key(self, root: str) -> Optional[str]:
        res = self.resources.get(root)
        if not res:
            return None

        released_versions = ['v5', 'v4', 'v3', 'v2', 'v1']
        suffix = '.' + res.kind
        candidates = [k for k in self.storage.keys() if k.endswith(suffix)]
        candidates.sort(key=lambda x: x.split('.')[-2], reverse=True)
        for v in released_versions:
            for candidate in candidates:
                if candidate.split('.')[-2] == v:
                    return candidate
        return candidates[0]

    def _load_doc(self, version: str):
        path = Path('data/{}/swagger.json'.format(version))
        if not path.exists():
            raise FileNotFoundError()

        with path.open() as f:
            doc_dict = json.load(f, object_pairs_hook=OrderedDict)
            definitions = doc_dict['definitions']
            for (key, detail) in definitions.items():
                item = DefItem.from_dict(self, detail)
                self.store(key, item)


class DefItem(object):

    def __init__(self):
        self.lookup = None
        self._type = ''
        self._ref_link = ''
        self._properties = OrderedDict()

    def search(self, path: str) -> Optional[DefItem]:
        if not path:
            return self

        if self.type != 'object' and self.type != 'array':
            return None

        root = path.split('.')[0]
        if self.type == 'array':
            if root != 'item':
                return None
            return self.array_item

        item = self.properties.get(root)
        if not item:
            return None

        parts = path.split('.', maxsplit=1)
        if len(parts) == 1:
            return item

        return item.search(parts[1])

    @classmethod
    def from_dict(cls, lookup: ApiDoc, raw: Dict[str, object]) -> Optional[DefItem]:
        item = DefItem()
        item.lookup = lookup
        item._description = raw.get('description', '')

        item._type = raw.get('type', '')
        if item._type in ['boolean', 'string']:
            return item

        if item._type in ['number', 'integer']:
            item._format = raw.get('format', '')
            return item

        if item._type == 'array':
            inner_item = raw.get('items', {})
            item._array_item = cls.from_dict(lookup, inner_item)
            return item

        if item._type != '' and item._type != 'object':
            print('Unknown item type: {}'.format(item._type))
            return None

        item._required = raw.get('required', [])

        ref_link = raw.get('$ref', '')
        if ref_link.startswith('#/definitions/'):
            ref_link = ref_link[len('#/definitions/'):]
        item._ref_link = ref_link
        if ref_link:
            return item

        raw_properties = raw.get('properties', OrderedDict())
        item._type = 'object'
        properties = OrderedDict()
        for (key, detail) in raw_properties.items():
            dict_item = cls.from_dict(lookup, detail)
            if dict_item:
                properties[key] = dict_item
        # if mark:
        #     print(properties)
        item._properties = properties

        # TODO deal with additionalProperties

        return item

    @property
    def def_id(self) -> str:
        return self._def_id

    @def_id.setter
    def def_id(self, value: str):
        self._def_id = value

    @property
    def ref_link(self) -> str:
        return self._ref_link

    @property
    def ref(self) -> DefItem:
        if self.ref_link and self.lookup:
            return self.lookup.fetch(self.ref_link)
        return None

    @property
    def description(self) -> str:
        if self._description:
            return self._description
        if self.ref:
            return self.ref.description
        return ''

    @property
    def type(self) -> str:
        if self._type:
            return self._type
        if self.ref:
            return self.ref.type
        return ''

    @property
    def format(self) -> str:
        if self.type in ['number', 'integer']:
            return self._format
        return ''

    @property
    def properties(self):
        if self._properties:
            return self._properties

        if self.ref:
            return self.ref.properties
        
        return self._properties

    @property
    def required(self) -> List[str]:
        return self._required

    @property
    def array_item(self):
        if not self.type == 'array':
            return None
        if self._array_item:
            return self._array_item
        if self.ref:
            return self.ref.array_item
        return None

    def to_dict(self):
        result = OrderedDict()
        result['description'] = self.description
        result['type'] = self.type
        if self.type in ['number', 'integer']:
            result['format'] = self.format
        if self.type == 'array':
            result['items'] = self.array_item.to_dict()
        if self.type == 'object':
            result['properties'] = OrderedDict()
            for (key, item) in self.properties.items():
                result['properties'][key] = item.to_dict()
            result['required'] = self.required
        return result


if __name__ == '__main__':
    doc = ApiDoc('1.13.7')
    rqs = doc.fetch('io.k8s.api.core.v1.ResourceQuotaStatus')
    item = doc.search('po.metadata')
    print(item.description)
    # print(item.ref_link)
    # print(item.ref)
    # print(item.ref.properties.keys())
    print(item.properties.keys())
    # print(json.dumps(rqs.to_dict(), indent=4))

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
