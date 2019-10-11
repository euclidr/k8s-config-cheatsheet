# -*- coding:utf-8 -*-
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
    if not item:
        abort(404)

    upper_item = None
    if len(rpath.split('.')) > 2:
        upper_item = doc.search('.'.join(rpath.split('.')[:-1]))

    ctx = {
        'version': ver,
        'item': item,
        'upper_item': upper_item,
        'resources': doc.resources.items()
    }

    return render_template('resource.jinja', **ctx)
