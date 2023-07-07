import json
from datetime import date, timedelta

from app.adapters.routes import *
from app.domain import KookSessionCounts, KookSessionCount
from app.utils.json_converters import json_dumps, json_loads
from domain.builders import aValidID, validKookCreationParameters, aValidKook, validKookkieSessionCreationParameters
from testing import *
from .routes_tests import RoutesTests, get_csrf_token, localhost_context


class TestKooksRoutes_Post(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        self.do_signin()

    def create_routes(self):
        self.create = Mock()
        self.create.return_value = Success(id=aValidID(33))
        return create_kook_routes(current_user_repository=self.current_user_repository, create=self.create).register(
            self.application)

    def test_post_kook_invokes_create_kook_command_with_body_parameters_and_kook(self):
        self.client.post('/api/kooks', data=json_dumps(validKookCreationParameters()), content_type='application/json')
        self.create.assert_called_with(validKookCreationParameters(), context=localhost_context(), user=aValidKook())

    def test_post_kook_responds_with_a_200_with_the_id_of_the_kook_when_successful(self):
        response = self.client.post('/api/kooks', data=json_dumps(validKookkieSessionCreationParameters()),
                                    content_type='application/json')
        assert_that(response.status, equal_to('201 CREATED'))
        assert_that(json_loads(response.data), equal_to(dict(id=str(aValidID(33)))))

    def test_post_kook_responds_with_an_error_when_command_fails(self):
        self.create.return_value = Failure(message="some-error-message")
        response = self.client.post('/api/kooks', data='{}', content_type='application/json')
        assert_that(response.status, equal_to('400 BAD REQUEST'))
        assert_that(json_loads(response.data), equal_to(dict(message="some-error-message")))


class TestKooksRoutes_Get(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        self.do_signin()

    def create_routes(self):
        self.all = Mock()
        self.all.return_value = Success(kooks=[aValidKook()])
        return create_kook_routes(current_user_repository=self.current_user_repository, all=self.all).register(self.app)

    def test_get_returns_all_kooks(self):
        response = self.client.get('/api/kooks')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json.loads(response.data), equal_to(as_kook_list([aValidKook()])))

    def test_issues_csrf_cookie(self):
        self.client.get('/api/kooks')
        assert get_csrf_token(self.client) is not None

    def test_invokes_query_with_current_kook(self):
        self.client.get('/api/kooks')
        self.all.assert_called_with(user=aValidKook())

    def test_responds_with_an_error_when_query_fails(self):
        self.all.return_value = Failure(message="some-error-message")
        response = self.client.get('/api/kooks')
        assert_that(response.status, equal_to('400 BAD REQUEST'))
        assert_that(json_loads(response.data), equal_to(dict(message="some-error-message")))


class TestKookRoutes_counts_per_kook(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.kook_session_counts = Mock()
        self.setup_app()
        self.do_signin()
        self.counts = KookSessionCounts(KookSessionCount(id=aValidID('1'), name="Henk", count=1))
        self.kook_session_counts.return_value = Success(counts=self.counts)

    def create_routes(self):
        self.repository = Mock()
        return create_kook_routes(current_user_repository=self.current_user_repository,
                                  kook_session_counts=self.kook_session_counts).register(self.app)

    def test_get_all_number_of_sessions_per_kook(self):
        response = self.client.get('/api/kooks-session-counts')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json_loads(response.data), equal_to(as_counts_list(self.counts)))

    def test_invokes_query_with_current_kook(self):
        self.client.get('/api/kooks-session-counts')
        self.kook_session_counts.assert_called_with(user=aValidKook(), since=None)

    def test_responds_with_an_error_when_query_fails(self):
        self.kook_session_counts.return_value = Failure(message="some-error-message")
        response = self.client.get('/api/kooks-session-counts')
        assert_that(response.status, equal_to('400 BAD REQUEST'))
        assert_that(json_loads(response.data), equal_to(dict(message="some-error-message")))


class TestKookRoutes_counts_per_kook_as_post(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.kook_session_counts = Mock()
        self.setup_app()
        self.do_signin()
        self.counts = KookSessionCounts(KookSessionCount(id=aValidID('1'), name="Henk", count=1))
        self.kook_session_counts.return_value = Success(counts=self.counts)

    def create_routes(self):
        self.repository = Mock()
        return create_kook_routes(current_user_repository=self.current_user_repository,
                                  kook_session_counts=self.kook_session_counts).register(self.app)

    def test_get_all_number_of_sessions_per_kook(self):
        response = self.client.post('/api/kooks-session-counts', data='{}', content_type='application/json')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json_loads(response.data), equal_to(as_counts_list(self.counts)))

    def test_invokes_query_with_current_kook(self):
        self.client.post('/api/kooks-session-counts', data='{}', content_type='application/json')
        self.kook_session_counts.assert_called_with(user=aValidKook(), since=None)

    def test_since_is_passed_as_timestamp(self):
        response = self.client.post('/api/kooks-session-counts', data=json_dumps(dict(since='2020-12-31')),
                                    content_type='application/json')
        self.kook_session_counts.assert_called_with(user=aValidKook(), since=Clock().parse_date('2020-12-31'))

    def test_responds_with_an_error_when_query_fails(self):
        self.kook_session_counts.return_value = Failure(message="some-error-message")
        response = self.client.post('/api/kooks-session-counts', data='{}', content_type='application/json')
        assert_that(response.status, equal_to('400 BAD REQUEST'))
        assert_that(json_loads(response.data), equal_to(dict(message="some-error-message")))


class TestMappingAListOfKooksToAListOfDicts:
    def test_creates_a_kookkie_session_list_item_for_each_kookkie_session(self):
        assert (as_kook_list([aValidKook(id=aValidID('1')), aValidKook(id=aValidID('2'))])
                == dict(kooks=[
                    as_kook(aValidKook(id=aValidID('1'))),
                    as_kook(aValidKook(id=aValidID('2')))]))


class TestMappingKookToItemDict:
    def test_creates_a_kook_who_has_not_accepted_terms_of_service(self):
        license_valid_date = date.today() + timedelta(days=1)
        kook = aValidKook(id=aValidID('1'), email='henk@kooks.com', name='F. Kook', is_admin=True)
        assert_that(as_kook(kook), equal_to(dict(
            id=str(aValidID('1')),
            name='F. Kook',
            email='henk@kooks.com',
            isAdmin=True)))

    def test_creates_a_kook_who_has_accepted_terms_of_service(self):
        license_valid_date = date.today() + timedelta(days=1)
        kook = aValidKook(id=aValidID('1'), email='henk@kooks.com', name='F. Kook', is_admin=False)
        assert_that(as_kook(kook), equal_to(dict(
            id=str(aValidID('1')),
            name='F. Kook',
            email='henk@kooks.com',
            isAdmin=False)))


class TestMappingAsKookSessionCounts:
    def test_creates_a_list_of_session_counts(self):
        assert_that(as_counts_list(KookSessionCounts(KookSessionCount(id=aValidID('3'), name='Henk', count=44))),
                    equal_to(
                        dict(kook_session_counts=[
                            dict(id=str(aValidID('3')), name='Henk', count=44)
                        ])
                    ))


def assert_cookie_set(response, cookie, value):
    assert '{}={}'.format(cookie, value) in response.headers['Set-Cookie']


def create_kook_routes(**kwargs):
    valid_route_params = dict(
        current_user_repository=None,
        create=None,
        all=None,
        kook_session_counts=None)
    return KooksRoutes(**{**valid_route_params, **kwargs})
