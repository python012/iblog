#  -*- coding: utf-8 -*-

from iblog.blurprint.auth import auth_bp
from iblog.blurprint.admin import admin_bp
from iblog.blurprint.blog import blog_bp
from iblog.extensions import bootstrap, db, moment, ckeditor, mail
from flask import Flask
from iblog.settings import config
import os


def create_app(config_name=None):
    """
    Factory function to generate flask instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('iblog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_error(app)

    return app


def register_template_context(app):
    pass


def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_logging(app):
    pass


def register_error(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_commands(app):
    pass
