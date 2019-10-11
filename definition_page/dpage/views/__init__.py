# -*- coding:utf-8 -*-

def init(app):
    from .resource import bp as resource_bp
    from .versions import bp as versions_bp
    app.register_blueprint(resource_bp)
    app.register_blueprint(versions_bp)
