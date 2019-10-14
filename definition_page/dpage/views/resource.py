# -*- coding:utf-8 -*-
from collections import OrderedDict
from flask import Blueprint, render_template, abort
from dpage.logic.apidoc import get_doc

bp = Blueprint('resource', __name__, url_prefix='/r')

@bp.route('/<ver>', methods=['GET'])
def index(ver):
    doc = get_doc(ver)
    if not doc:
        abort(404)
    ctx = {
        'version': ver,
        'resources': doc.resources.items()
    }
    return render_template('resources.jinja', **ctx)


@bp.route('/<ver>/<rpath>')
def doc(ver, rpath):
    doc = get_doc(ver)
    if not doc:
        abort(404)

    item = doc.search(rpath)
    print(item)
    if not item:
        abort(404)

    kind = doc.get_root_kind(rpath)
    item_name = kind

    if len(rpath.split('.')) > 1:
        item_name = rpath.split('.')[-1]

    upper_item = None
    upper_name = None
    upper_rpath = None
    if len(rpath.split('.')) >= 2:
        upper_name = rpath.split('.')[-2]
        upper_rpath = '.'.join(rpath.split('.')[:-1])
        upper_item = doc.search('.'.join(rpath.split('.')[:-1]))

    if len(rpath.split('.')) == 2:
        upper_name = kind

    resources = doc.resources.items()
    res_groups = OrderedDict()
    for r in resources:
        if r.api_group in res_groups:
            res_groups[r.api_group].append(r)
        else:
            res_groups[r.api_group] = [r]

    ctx = {
        'version': ver,
        'rpath': rpath,
        'kind': kind,
        'item': item,
        'item_name': item_name,
        'upper_item': upper_item,
        'upper_name': upper_name,
        'upper_rpath': upper_rpath,
        'res_groups': res_groups,
    }

    return render_template('resource.jinja', **ctx)
