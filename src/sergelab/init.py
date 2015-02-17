
import importlib

from flask import Flask, Blueprint
from flask.ext.babel import Babel
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.collect import Collect
from flask.ext.mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension


class MyCollect(Collect, object):
    def init_app(self, app):
        super(MyCollect, self).init_app(app)
        self.blueprints['__app'] = app


# Extensions
babel = Babel()
assets = Environment()
db = SQLAlchemy()
collect = MyCollect()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config/base.cfg')
    app.config.from_envvar('FLASK_SETTINGS')

    # TODO: Debug logging

    babel.init_app(app)
    assets.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    return app


def init_extensions(app):
    collect.init_app(app)

    # Enable the DebugToolbar
    if app.config['DEBUG_TOOLBAR']:
        app.config['DEBUG_TB_PANELS'] = [
            'flask_debugtoolbar.panels.versions.VersionDebugPanel',
            'flask_debugtoolbar.panels.timer.TimerDebugPanel',
            'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
            'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
            'flask_debugtoolbar.panels.template.TemplateDebugPanel',
            'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
            'flask_debugtoolbar.panels.logger.LoggingPanel',
            'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        ]
        DebugToolbarExtension(app)


def register_blueprints(app):
    rv = []

    if not app.config['BLUEPRINTS']:
        app.config['BLUEPRINTS'] = []

    for name in app.config['BLUEPRINTS']:
        m = importlib.import_module(name + '.views')
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
                app.logger.debug('Blueprint {0} registered'.format(name))
                rv.append(item)
    return rv


app = create_app()
with app.app_context():
    register_blueprints(app)
    init_extensions(app)


import views  # pyflake8: noqa
import models  # pyflake8: noqa
