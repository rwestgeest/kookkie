from typing import TypeAlias, Type

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix
from dataclasses import dataclass
from paste.translogger import TransLogger
from app.domain import FrontEndContext
import logging

from config import Config

db: SQLAlchemy = SQLAlchemy()
Model: TypeAlias = db.Model  # type: ignore
migrate: Migrate = Migrate()

nr_of_load_balancers = 2


def configure_logger():
    simple_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(simple_formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    return handler


def create_app(config: Type[Config]):
    logger_handler = configure_logger()
    app = Flask(__name__)
    app.config.from_object(config)
    app.wsgi_app = TransLogger(ProxyFix(app.wsgi_app, x_for=nr_of_load_balancers, x_proto=0))  # type: ignore
    csrf = CSRFProtect(app)
    app.logger.setLevel(logging.DEBUG)
    @app.after_request
    def log_request_info(f):
        app.logger.debug('Headers: %s', request.headers)
        return f

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify(message='please reload the page or sign in again'), 400 
    db.init_app(app)
    migrate.init_app(app, db)
    return Application(app, csrf, db, config, logger_handler)


@dataclass(frozen=True)
class Application:
    app: Flask
    csrf: CSRFProtect
    db: SQLAlchemy
    config: Type[Config]
    logger_handler: logging.Handler

    def route(self, rule, **options):
        return self.app.route(rule, **options)

    def test_client(self):
        return self.app.test_client()

    def app_context(self):
        return self.app.app_context()

    def front_end_context(self, request):
        return FrontEndContext(request.url_root, https=self.config.HTTPS_LINKS)
