from domain.commands.null_command import NullCommand
from testing import *
from app.utils.json_converters import json_dumps, json_loads
from domain.builders import *
from app.domain import *
from app.adapters.routes import *
from .routes_tests import RoutesTests, get_csrf_token, localhost_context
from textwrap import dedent


class TestKookkieSessionRoutes_Post(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        self.do_signin()
        
    def create_routes(self):
        self.create_kookkie_session = Mock()
        self.create_kookkie_session.return_value = Success(id=aValidID(33))

        return create_kookkie_session_routes(create_kookkie_session=self.create_kookkie_session, current_user_repository=self.current_user_repository).register(self.application)

    def test_post_kookkie_session_invokes_create_kookkie_session_command_with_body_parameters_and_kook(self):
        self.client.post('/api/kookkie-sessions', data=json_dumps(validKookkieSessionCreationParameters()), content_type='application/json')
        self.create_kookkie_session.assert_called_with(validKookkieSessionCreationParameters(kook=aValidKook()))

    def test_post_kookkie_session_responds_with_a_200_with_the_id_of_the_kookkie_session_when_successful(self):
        response = self.client.post('/api/kookkie-sessions', data=json_dumps(validKookkieSessionCreationParameters()), content_type='application/json')
        assert response.status == '201 CREATED'
        assert json_loads(response.data) == dict(id=str(aValidID(33)))

    def test_post_kookkie_session_responds_with_an_error_when_command_fails(self):
        self.create_kookkie_session.return_value = Failure(message="some-error-message")
        response = self.client.post('/api/kookkie-sessions', data='{}', content_type='application/json')
        assert response.status == '400 BAD REQUEST'
        assert json_loads(response.data) == dict(message="some-error-message")


def sign_in(client, username='anyone', password='password'):
    client.post('/api/login', data=json_dumps(dict(username=username, password=password)),
                content_type='application/json')


def assert_cookie_set(response, cookie, value):
    assert '{}={}'.format(cookie, value) in response.headers['Set-Cookie']


def create_kookkie_session_routes(**kwargs):
    valid_route_params = dict(kookkie_session_repository=None,
                              current_user_repository=None,
                              create_kookkie_session=None)
    print({**valid_route_params, **kwargs})
    return KookkieSessionRoutes(**{**valid_route_params, **kwargs})
