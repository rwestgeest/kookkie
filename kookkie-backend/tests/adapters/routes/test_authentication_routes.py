from app.domain import PasswordResetToken
from domain.commands.null_command import NullCommand
from testing import *
from flask_login import login_required
from app.utils.json_converters import json_dumps, json_loads
from domain.builders import aValidKook, aValidID
from app.adapters.routes import *
from .dummy_authenticator import StubbedKookRepository
from .routes_tests import RoutesTests, get_csrf_token, localhost_context


class FakeUserRepository(KookRepository):
    def by_username(self, username):
        if username == 'henk': return aValidKook()
        if username == 'blocked_user': return aValidKook(is_blocked=True)
        return None

    def by_id_with_result(self, id: ID):
        return Success(kook=aValidKook())

    def has_user(self, username): pass
    def by_username_with_result(self, username: str): pass
    def by_token(self, token: PasswordResetToken): pass
    def all(self): pass
    def save(self, kook: Kook): pass
    def remove(self, id: ID): pass


def register_authenticated_bla_route(app):
    @app.route('/api/bla', methods=['GET'])
    @login_required
    def bla():
        return jsonify({})


def aSignin(app):
    user_repository = FakeUserRepository()
    current_user_repository = FlaskLoginBasedCurrentUserRepository(user_repository).register(app)
    return Signin(user_repository, current_user_repository)


class TestAuthenticationRoutes_CSRF(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app(check_csrf=True)
        register_authenticated_bla_route(self.app)
    
    def create_routes(self):
        sign_in = aSignin(self.app)
        return create_authentication_routes(sign_in=sign_in, reset_password=lambda **kwargs: Success(),
                                            request_password_reset=lambda **kwargs: Success()).register(self.application)

    def test_does_not_check_csrf_on_login(self):
        response = sign_in(self.client, 'henk', 'password')
        assert response.status == '200 OK'

    def test_issues_csrf_cookie_on_login(self):
        sign_in(self.client, 'henk', 'password')
        assert get_csrf_token(self.client) is not None

    def test_does_not_check_csrf_on_password_reset_request(self):
        response = self.client.post('/api/request-password-reset', data=json_dumps(dict(username='john@doe.eu')), content_type='application/json')
        assert response.status == '200 OK'

    def test_does_not_check_csrf_on_reset_password(self):
        response = self.client.post('/api/resetpassword', data=json_dumps(dict(new_password='new-password', token=str(aValidID('444')))), content_type='application/json')
        assert response.status == '200 OK'


class TestAuthenticationRoutesAuthentication(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        register_authenticated_bla_route(self.app)
    
    def create_routes(self):
        sign_in = aSignin(self.app)
        return create_authentication_routes(sign_in=sign_in).register(self.application)

    def test_fails_when_not_authenticated(self):
        response = self.client.get('/api/bla')
        assert response.status == '401 UNAUTHORIZED'

    def test_fails_when_user_not_known(self):
        sign_in(self.client, 'piet@qwan.eu', 'password')
        response = self.client.get('/api/bla')
        assert response.status == '401 UNAUTHORIZED'

    def test_fails_when_password_is_incorrect(self):
        sign_in(self.client, 'henk', 'wrong')
        response = self.client.get('/api/bla')
        assert response.status == '401 UNAUTHORIZED'

    def test_passes_when_authenticated(self):
        sign_in(self.client, 'henk', 'password')
        response = self.client.get('/api/bla')
        assert response.status == '200 OK'

    def test_sign_in_responds_with_ok_when_successful(self):
        response = sign_in(self.client, 'henk', 'password')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json_loads(response.data), equal_to({}))

    def test_sign_in_responds_with_401_with_username_password_incorrect_on_failure(self):
        response = sign_in(self.client, 'piet', 'password')
        assert_that(response.status, equal_to('401 UNAUTHORIZED'))
        assert_that(json_loads(response.data), equal_to(dict(messageId='error.authentication.userNameOrPasswordIncorrect')))
    

class TestAuthenticationRoutesLogout(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        register_authenticated_bla_route(self.app)

    def create_routes(self):
        current_user_repository = FlaskLoginBasedCurrentUserRepository(FakeUserRepository()).register(self.app)
        sign_in = Signin(FakeUserRepository(), current_user_repository)
        sign_out = Signout(current_user_repository)
        return create_authentication_routes(sign_in=sign_in, sign_out=sign_out).register(self.application)

    def test_cannot_access_authenticated_route_after_logout(self):
        sign_in(self.client, 'henk', 'password')
        self.client.get('/api/logout')
        response = self.client.get('/api/bla')
        assert response.status == '401 UNAUTHORIZED'

    def test_logout_redirects_to_the_root_url(self):
        sign_in(self.client, 'henk', 'password')
        response = self.client.get('/api/logout')
        assert response.status == '302 FOUND'
        assert response.location == '/'

    def test_can_logout_while_not_signed_in(self):
        response = self.client.get('/api/logout')
        assert response.status == '302 FOUND'


def sign_in(client, username, password):
    return client.post('/api/login', data=json_dumps(dict(username=username, password=password)), content_type='application/json')


class TestAuthenticationRoutesRequestResetPassword(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()

    def create_routes(self):
        self.kook_repository = StubbedKookRepository()
        self.request_password_reset = NullCommand()
        return create_authentication_routes(request_password_reset=self.request_password_reset).register(self.application)

    def test_invokes_request_password_reset_command(self):
        self.client.post('/api/request-password-reset', data=json_dumps(dict(username='john@doe.eu')),
                         content_type='application/json')
        assert_that(self.request_password_reset.called_with,
                    equal_to({'username': 'john@doe.eu', 'context': localhost_context()}))

    def test_succeeds_when_username_is_given(self):
        response = self.client.post('/api/request-password-reset', data=json_dumps(dict(username='garbledigook')), content_type='application/json')
        assert response.status == '200 OK'


class TestAuthenticationRoutesResetPassword(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()

    def create_routes(self):
        self.kook_repository = StubbedKookRepository()
        self.reset_password = NullCommand()
        self.check_reset_password_token = NullCommand()
        return create_authentication_routes(reset_password=self.reset_password,
                                            check_reset_password_token=self.check_reset_password_token)\
            .register(self.application)

    def test_returns_ok_when_token_check_succeeds(self):
        response = self.client.get('/api/resetpassword/{}'.format(aValidID('1')))
        assert response.status == '200 OK'
        assert_that(self.check_reset_password_token.called_with, equal_to(dict(token=aValidID('1'))))

    def test_returns_not_found_when_token_check_fails(self):
        self.check_reset_password_token.will_fail()
        response = self.client.get('/api/resetpassword/{}'.format(aValidID('1')))
        assert response.status == '404 NOT FOUND'

    def test_invokes_reset_password_command(self):
        self.client.post('/api/resetpassword', data=json_dumps(dict(new_password='new-password',
                                                                    token=str(aValidID('444')))),
                         content_type='application/json')
        assert_that(self.reset_password.called_with, equal_to(dict(new_password='new-password', token=aValidID('444'))))

    def test_succeeds_when_reset_password_is_successful(self):
        response = self.client.post('/api/resetpassword', data=json_dumps(dict(new_password='new-password', token=str(aValidID('444')))), content_type='application/json')
        assert response.status == '200 OK'

    def test_fails_when_reset_password_fails(self):
        self.reset_password.will_fail()
        response = self.client.post('/api/resetpassword', data=json_dumps(dict(new_password='new-password', token=str(aValidID('444')))), content_type='application/json')
        assert response.status == '400 BAD REQUEST'
        assert json_loads(response.data) == dict(message='failed')


def create_authentication_routes(**kwargs):
    valid_parameters = dict(sign_in=None, sign_out=None, request_password_reset=None, reset_password=None, check_reset_password_token=None)
    return AuthenticationRoutes(**{**valid_parameters, **kwargs})
