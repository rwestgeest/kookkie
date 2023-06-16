import logging
from hamcrest import assert_that, empty
from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from app.adapters.routes import FlaskLoginBasedCurrentUserRepository
from .dummy_authenticator import StubbedKookRepository
from app import Application
from app.domain import FrontEndContext
from app.domain.commands import Signin
from app.adapters.routes.route_builder import RouteBuilder


def get_csrf_token(client):
    return next((cookie for cookie in client.cookie_jar if cookie.name == RouteBuilder.XSRF_COOKIE_NAME), None)


def localhost_context():
    return FrontEndContext('https://localhost/')


class TestConfig:
    SECRET_KEY = 'g@rbl3dIg00k'
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True
    WTF_CSRF_HEADERS = ['X-XSRF-Token']
    HTTPS_LINKS = True


class TestConfigWithCsrf(TestConfig):
    WTF_CSRF_CHECK_DEFAULT = True


class RoutesTests:
    def setup_app(self, check_csrf=False):
        self.app = Flask(__name__)
        if check_csrf:
            self.app.config.from_object(TestConfigWithCsrf)
        else:
            self.app.config.from_object(TestConfig)
        csrf = CSRFProtect(self.app)
        self.application = Application(self.app, csrf=csrf, db=None, config=TestConfig, logger_handler=None)
        self.client = self.app.test_client()
        self.current_user_repository = FlaskLoginBasedCurrentUserRepository(StubbedKookRepository()).register(self.app)
        self.authenticator = self.current_user_repository
        self.signin = Signin(user_repository=StubbedKookRepository(), current_user_repository=self.current_user_repository)
        self.routes_registry = self.create_routes()
        logging.getLogger().setLevel(logging.ERROR)

    def test_all_routes_have_login_required_specified(self):
        assert_that(self.routes_registry.unspecified_logins, empty())

    def do_signin(self):
        @self.app.route('/login_for_test', methods=['POST'])
        def login():
            self.signin('username', 'password')
            return jsonify({})
        self.client.post('/login_for_test')
