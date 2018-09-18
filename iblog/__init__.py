#  -*- coding: utf-8 -*-

from iblog.blurprint.auth import auth_bp
from iblog.blurprint.admin import admin_bp
from iblog.blurprint.blog import blog_bp
from iblog.extensions import bootstrap, db, moment, ckeditor, mail
from flask import Flask
from iblog.settings import config
import os
import click


def create_app(config_name=None):
    """
    Factory function to generate flask instance, will be found
    once `flask run`.
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
    register_shell_context(app)

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

    @app.cli.command()
    @click.option('--category', default=10, help='create 10 categories by default')
    @click.option('--post', default=50, help='create 50 posts by default')
    @click.option('--comment', default=500, help='create 500 comments by default')
    def init(category, post, comment):
        """
        Generate the fake data including categories, posts and comments.
        """
        from iblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments
        db.drop_all()
        db.create_all()

        click.echo('Creating adminstrator...')
        fake_admin()

        click.echo('Create %d categories...' % category)
        fake_categories()

        click.echo('Create %d posts...' % post)
        fake_posts(post)

        click.echo('Create %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')
