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

    # check if name is ambiguous
    first_part = rpath.split('.')[0]
    if doc.resources.is_ambiguous(first_part):
        choices = doc.resources.resources_by_key(first_part)
        subseq = ''
        if len(rpath.split('.')) > 1:
            subseq = '.'.join(rpath.split('.')[1:])
        ctx = dict(
            version=ver,
            name=first_part,
            subseq=subseq,
            choices=choices,
        )
        return render_template('ambiguous_resources.jinja', **ctx)

    item = doc.search(rpath)
    if not item:
        abort(404)

    root_resource = doc.resources.get(first_part)

    rpath = '.'.join([root_resource.id] + rpath.split('.')[1:])
    is_root_resource = len(rpath.split('.')) == 1
    kind = doc.get_root_kind(rpath)
    api_group = doc.get_root_group(rpath)
    api_version = doc.get_root_version(rpath)
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
        'is_root_resource': is_root_resource,
        'kind': kind,
        'api_group': api_group,
        'api_version': api_version,
        'item': item,
        'item_name': item_name,
        'upper_item': upper_item,
        'upper_name': upper_name,
        'upper_rpath': upper_rpath,
        'res_groups': res_groups,
    }

    return render_template('resource.jinja', **ctx)
