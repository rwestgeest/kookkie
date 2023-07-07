from app.adapters.repositories import InMemoryKookkieSessionsRepository
from app.adapters.routes import *
from app.utils.json_converters import json_dumps, json_loads
from domain.builders import aValidID, validKookkieSessionCreationParameters, aValidKook, aValidKookkieSession, \
    aValidJoinInfo
from testing import *
from .routes_tests import RoutesTests


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

    def test_post_kookkie_session_responds_with_a_201_with_the_id_of_the_kookkie_session_when_successful(self):
        response = self.client.post('/api/kookkie-sessions', data=json_dumps(validKookkieSessionCreationParameters()), content_type='application/json')
        assert response.status == '201 CREATED'
        assert json_loads(response.data) == dict(id=str(aValidID(33)))

    def test_post_kookkie_session_responds_with_an_error_when_command_fails(self):
        self.create_kookkie_session.return_value = Failure(message="some-error-message")
        response = self.client.post('/api/kookkie-sessions', data='{}', content_type='application/json')
        assert response.status == '400 BAD REQUEST'
        assert json_loads(response.data) == dict(message="some-error-message")


class TestKookkieSessionRoutes_GetAll(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        self.do_signin()

    def create_routes(self):
        self.repository = InMemoryKookkieSessionsRepository(kookkie_sessions=[
            aValidKookkieSession(id=aValidID("123"), kook_id=aValidID("11")),
            aValidKookkieSession(id=aValidID("456"), kook_id=aValidKook().id)
        ])
        return create_kookkie_session_routes(kookkie_session_repository=self.repository, current_user_repository=self.current_user_repository).register(self.application)

    def test_returns_kookkies_for_the_current_signed_in_kook(self):
        response = self.client.get('/api/kookkie-sessions', content_type='application/json')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json_loads(response.data), equal_to(as_kookkie_list([aValidKookkieSession(id=aValidID("456"), kook_id=aValidKook().id).as_list_item()])))



class TestKookkieSessionRoutes_Start(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        self.do_signin()

    def create_routes(self):
        self.start_kookkie_session = Mock()
        self.returned_join_info = aValidJoinInfo()
        self.start_kookkie_session.return_value = Success(started_kookkie=self.returned_join_info)

        return create_kookkie_session_routes(start_kookkie_session=self.start_kookkie_session,
                                             current_user_repository=self.current_user_repository)\
            .register(self.application)

    def test_post_kookkie_session_start_invokes_start(self):
        self.client.post('/api/kookkie-sessions/{}/start'.format(str(aValidID(123))), data='{}', content_type='application/json')
        self.start_kookkie_session.assert_called_with(kookkie_id=aValidID(123), kook=aValidKook())

    def test_post_kookkie_start_results_in_joining_info_when_successful(self):
        response = self.client.post('/api/kookkie-sessions/{}/start'.format(str(aValidID(123))), data='{}', content_type='application/json')
        assert response.status == '201 CREATED'
        assert_that(json_loads(response.data), equal_to(dict(as_started_kookkie(self.returned_join_info))))

    def test_post_kookkie_start_responds_with_an_error_when_command_fails(self):
        self.start_kookkie_session.return_value = Failure(message="some-error-message")
        response = self.client.post('/api/kookkie-sessions/{}/start'.format(str(aValidID(123))), data='{}', content_type='application/json')
        assert response.status == '400 BAD REQUEST'
        assert json_loads(response.data) == dict(message="some-error-message")


class TestMapStartedKookkie:
    def test_contains_the_kookkie(self):
        kookkie_session = aValidKookkieSession()
        result = as_started_kookkie(aValidJoinInfo(kookkie=kookkie_session, jwt=b'jwt', room_name="some_room"))
        assert_that(result, equal_to(dict(jwt='jwt', room_name='some_room', kookkie=as_kookkie_session(kookkie_session))))

class TestMapKookkie:
    def test_contains_all_kookkie_attributes(self):
        kookkie_session = aValidKookkieSession()
        result = as_kookkie_session(kookkie_session)
        assert_that(result, equal_to(dict(id=str(kookkie_session.id),
                                          name=kookkie_session.name,
                                          date=kookkie_session.date,
                                          kook_name=kookkie_session.kook_name)))

def sign_in(client, username='anyone', password='password'):
    client.post('/api/login', data=json_dumps(dict(username=username, password=password)),
                content_type='application/json')


def assert_cookie_set(response, cookie, value):
    assert '{}={}'.format(cookie, value) in response.headers['Set-Cookie']


def create_kookkie_session_routes(**kwargs):
    valid_route_params = dict(kookkie_session_repository=None,
                              current_user_repository=None,
                              create_kookkie_session=None,
                              start_kookkie_session=None)
    print({**valid_route_params, **kwargs})
    return KookkieSessionRoutes(**{**valid_route_params, **kwargs})
