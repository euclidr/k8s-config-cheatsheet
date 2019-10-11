#! -*- coding:utf-8 -*-
from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import List, Optional


class Resources(object):

    def __init__(self, version: str):
        self.name_mapper = OrderedDict()
        self.kind_mapper = {}
        self.short_mapper = {}
        self._load_resources(version)

    def _load_resources(self, version: str):
        path = Path('data/{}/api-resources.txt'.format(version))
        if not path.exists():
            raise FileNotFoundError()

        with path.open() as f:
            head = f.readline()
            col_widths = self._extract_col_widths(head)
            print(col_widths)
            for l in f:
                resource = self._extract_resource(l, col_widths)
                if resource:
                    self.add(resource)

        return self

    def items(self):
        return self.name_mapper.values()

    def add(self, res: Resource):
        self.name_mapper[res.name] = res
        self.kind_mapper[res.kind] = res
        if res.short_names:
            for short_name in res.short_names.split(','):
                self.short_mapper[short_name] = res

    def get_by_name(self, name: str) -> Optional[Resource]:
        return self.name_mapper.get(name)

    def get_by_short(self, short: str) -> Optional[Resource]:
        return self.short_mapper.get(short)

    def get_by_kind(self, kind: str) -> Optional[Resource]:
        return self.kind_mapper.get(kind)

    def get(self, key: str) -> Optional[Resource]:
        r = self.get_by_name(key)
        if r:
            return r
        r = self.get_by_kind(key)
        if r:
            return r
        return self.get_by_short(key)

    @staticmethod
    def _extract_resource(l: str, col_widths: List[int]) -> Resource:
        min_col_width = sum(col_widths)
        if len(l) < min_col_width:
            return None

        NAME, SHORTNAME, APIGROUP, NAMESPACED = 0, 1, 2, 3

        name = l[:col_widths[NAME]].strip()
        l = l[col_widths[NAME]:]

        short_names = l[:col_widths[SHORTNAME]].strip()
        l = l[col_widths[SHORTNAME]:]

        api_group = l[:col_widths[APIGROUP]].strip()
        l = l[col_widths[APIGROUP]:]

        namespaced = l[:col_widths[NAMESPACED]].strip()
        namespaced = True if namespaced == 'true' else False
        l = l[col_widths[NAMESPACED]:]

        kind = l.strip()
        if not kind:
            return None

        r = Resource()
        r.name = name
        r.short_names = short_names
        r.api_group = api_group
        r.namespaced = namespaced
        r.kind = kind
        return r


    @staticmethod
    def _extract_col_widths(head: str) -> List[int]:
        '''get column width except for the last column'''
        pre_blank, pre_idx = False, 0
        result = []
        for i, c in enumerate(head):
            if pre_blank and c != ' ':
                result.append(i-pre_idx)
                pre_idx = i
            pre_blank = c == ' '
        return result



class Resource(object):

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def short_names(self) -> str:
        return self._short_names

    @short_names.setter
    def short_names(self, value: str):
        self._short_names = value

    @property
    def api_group(self) -> str:
        return self._api_group

    @api_group.setter
    def api_group(self, value: str):
        self._api_group = value if value else 'core'

    @property
    def namespaced(self) -> bool:
        return self._namespaced

    @namespaced.setter
    def namespaced(self, value: bool):
        self._namespaced = value

    @property
    def kind(self) -> str:
        return self._kind

    @kind.setter
    def kind(self, value: str):
        self._kind = value

    def __repr__(self):
        return "Resource(name: {}, kind: {} short_names: {}, api_group: {}, namespaced: {})".format(
            self.name, self.kind, self.short_names, self.api_group, self.namespaced
        )



if __name__ == '__main__':
    Resources('1.13.7')
