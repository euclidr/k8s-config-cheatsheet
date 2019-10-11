from flask import Blueprint, render_template

bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def versions():
    ctx = {
        'vers': ['1.13.7']
    }
    return render_template('versions.jinja', **ctx)
