import logging
import sys

from flask import Flask
from app import commands
from app.extensions import (
    bcrypt,
    db,
    api,
    debug_toolbar,
    migrate,
)

from app.main.controller.wallet_controller import ns as wallet_ns
from app.main.controller.transaction_controller import ns as transaction_ns


def create_app(config_object="app.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_errorhandlers(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(wallet_ns)
    api.add_namespace(transaction_ns)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
