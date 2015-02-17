# coding: utf-8

from flask import current_app
from flask.ext.script import Server, Manager
from flask.ext.script.commands import Clean, ShowUrls
from flask.ext.assets import ManageAssets
from flask.ext.alembic import ManageMigrations

#from brpr.blueprints.language.manage import MakeMessage, CompileMessage

from sergelab.init import app, collect, db


manager = Manager(app)
manager.add_command('clean', Clean())
manager.add_command('routes', ShowUrls())
#manager.add_command('makemessages', MakeMessage('sergelab'))
#manager.add_command('compilemessages', CompileMessage('sergelab'))
manager.add_command('runserver', Server())
manager.add_command('migrate', ManageMigrations())
manager.add_command('assets', ManageAssets())
collect.init_script(manager)


@manager.command
def fastcgi():
    """ Run application as fastcgi """
    from flup.server.fcgi import WSGIServer

    class ScriptNameStripper(object):
        def __init__(self, app):
            self.app = app

        def __call__(self, environ, start_response):
            environ['SCRIPT_NAME'] = ''
            return self.app(environ, start_response)

    wapp = ScriptNameStripper(app)
    WSGIServer(wapp).run()


@manager.command
def syncdb(console=True):
    db.create_all()
    db.session.commit()


def main():
    manager.run()
