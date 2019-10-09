#! -*- coding:utf-8 -*-
from pathlib import Path
from typing import List


class Resource:

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def short_name(self) -> str:
        return self._short_name

    @short_name.setter
    def short_name(self, value: str):
        self._short_name = value

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
        return "Resource(name: {}, kind: {} short_name: {}, api_group: {}, namespaced: {})".format(
            self.name, self.kind, self.short_name, self.api_group, self.namespaced
        )


def load_resource(version: str):
    path = Path('data/{}/api-resources.txt'.format(version))
    if not path.exists():
        raise FileNotFoundError()
    with path.open() as f:
        head = f.readline()
        col_widths = _extract_col_widths(head)
        print(col_widths)
        for l in f:
            resource = _extract_resource(l, col_widths)
            print(resource)


def _extract_resource(l: str, col_widths: List[int]) -> Resource:
    min_col_width = sum(col_widths)
    if len(l) < min_col_width:
        return None

    NAME, SHORTNAME, APIGROUP, NAMESPACED = 0, 1, 2, 3

    name = l[:col_widths[NAME]].strip()
    l = l[col_widths[NAME]:]

    short_name = l[:col_widths[SHORTNAME]].strip()
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
    r.short_name = short_name
    r.api_group = api_group
    r.namespaced = namespaced
    r.kind = kind
    return r


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


if __name__ == '__main__':
    load_resource('1.13.7')
