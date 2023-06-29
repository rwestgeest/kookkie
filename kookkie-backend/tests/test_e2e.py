import pytest
import json
from boot import main
from domain.builders import *
from app.domain import PasswordHasher, KookkieSessionCreator
from app.adapters.repositories import InMemoryKookkieSessionsRepository
from app.domain.repositories import InMemoryKookRepository
from app.adapters.metrics import MetricsCollectorCreator
from app.utils.json_converters import json_dumps
from quiltz.testsupport.smtp import StubSmtpServer
from hamcrest import assert_that, contains_string, equal_to, is_in, is_not
from support.probe import probe_that
from app.adapters.routes import RouteBuilder
from adapters.routes.routes_tests import get_csrf_token


class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'g@rbl3dIg00k'
    SMTP_HOST = 'localhost'
    SMTP_PORT = '2625'
    MAIL_FROM = 'no-reply@qwan.eu'
    FOR_TEST = True
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True
    WTF_CSRF_HEADERS = ['X-XSRF-Token']
    HTTPS_LINKS = True


class XTestE2EAdmin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.smtp_server = StubSmtpServer(hostname=TestConfig.SMTP_HOST, port=TestConfig.SMTP_PORT)
        kook_repository = InMemoryKookRepository([aValidAdministrator()])
        app = main(config=TestConfig,
                   kookkie_session_repository=InMemoryKookkieSessionsRepository.with_hard_coded_values(),
                   kook_repository=kook_repository,
                   metricsCollectorCreator=MetricsCollectorCreator.forTest())
        self.client = app.test_client()
        self.smtp_server.start()
        yield
        self.smtp_server.stop()

    def test_sign_in_provides_csrf_token(self):
        response = self.client.post('/api/login', data=json_dumps(dict(username='admin@kooks.com',
                                                                       password='password')), content_type='application/json')
        assert_ok(response)
        assert_that(RouteBuilder.XSRF_COOKIE_NAME, is_in(response.headers['Set-Cookie']))
        
    def test_can_create_a_kookkie_session_when_authorized(self):
        self.client.post('/api/login', data=json_dumps(dict(username='admin@kooks.com', password='password')),
                         content_type='application/json')
        response_created = self.client.post('/api/kookkie-sessions',
                                            data=json.dumps(dict(date='2022-07-15', participant_count='3')),
                                            content_type='application/json',
                                            headers=csrf_headers(self.client))
        assert_created(response_created)
        id = json.loads(response_created.data)['id']
        response = self.client.get('/api/kookkie-sessions/{id}'.format(id = id))
        assert_ok(response)
        assert_that(json.loads(response.data)['team'], equal_to('T1'))

    def test_can_count_sessions_per_kook_when_authorized(self):        
        self.client.post('/api/login', data=json_dumps(dict(username='admin@kooks.com', password='password')),
                         content_type='application/json')
        response_all = self.client.get('/api/kooks-session-counts')
        assert_ok(response_all)
        assert_that(json.loads(response_all.data),
                    equal_to(dict(kook_session_counts=[{'count': 2, 'id': 'a8487ed5-39b4-48da-bf9a-a536e937a85a',
                                                               'name': 'Rob Westgeest'}])))


class TestE2EKookManagement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.smtp_server = StubSmtpServer(hostname=TestConfig.SMTP_HOST, port=TestConfig.SMTP_PORT)
        self.kook_repository = InMemoryKookRepository(
            [aValidAdministrator(), aValidKook(id=aValidID('456'))])
        app = main(config=TestConfig,
                   kookkie_session_repository=InMemoryKookkieSessionsRepository.with_hard_coded_values(),
                   kook_repository=self.kook_repository,
                   metricsCollectorCreator=MetricsCollectorCreator.forTest())
        self.client = app.test_client()
        self.smtp_server.start()
        self.admin_login = json_dumps(dict(username='admin@kooks.com', password='password'))
        yield
        self.smtp_server.stop()

    def test_can_create_a_kook_when_authorized(self):
        self.client.post('/api/login', data=self.admin_login, content_type='application/json')
        response_created = self.client.post('/api/kooks',
                                            data=json.dumps(validKookCreationParameters(email="gijs@kooks.org")),
                                            content_type='application/json',
                                            headers=csrf_headers(self.client))
        assert_created(response_created)
        id = json.loads(response_created.data)['id']
        probe_that(lambda: assert_that(self.smtp_server.messages[0], contains_string('gijs@kooks.org')))
        response_all = self.client.get('/api/kooks')
        assert_ok(response_all)
        assert_that({ kook['id']: kook for kook in json.loads(response_all.data)['kooks'] }[id]['email'], equal_to('gijs@kooks.org'))


class TestE2EParticipants:
    @pytest.fixture(autouse=True)
    def setup(self):
        kook_repository = InMemoryKookRepository([aValidKook(email='henk@qwan.eu', hashed_password=PasswordHasher().hash('password'))])
        self.kookkie_session_repo=InMemoryKookkieSessionsRepository()
        app = main(config=TestConfig, kookkie_session_repository=self.kookkie_session_repo, kook_repository=kook_repository, metricsCollectorCreator=MetricsCollectorCreator.forTest())
        self.participant_client = app.test_client()
        self.kook_client = app.test_client()
        self.kook_client.post('/api/login', data=json.dumps(dict(username='henk@qwan.eu', password='password')), content_type='application/json')

    def test_can_join_a_session(self):
        kookkie_session = self.save_kookkie_session(KookkieSessionCreator().create_with_id(**validKookkieSessionCreationParameters()).kookkie_session_created)
        response = self.participant_client.post('/api/kookkie-sessions/{id}/join'.format(id = kookkie_session.id))
        assert_created(response)
        assert json.loads(response.data)['kook_name'] == kookkie_session.kook_name

    def save_kookkie_session(self, session_created):
        self.kookkie_session_repo.save(session_created)
        return session_created.kookkie_session


class TestE2EAuthentication:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.smtp_server = StubSmtpServer(hostname=TestConfig.SMTP_HOST, port=TestConfig.SMTP_PORT)
        self.token = aValidPasswordResetToken(token=aValidID('222'))
        self.kook_repository = InMemoryKookRepository([aValidKook(email='henk@qwan.eu', password_reset_token=self.token)])
        self.kookkie_session_repo = InMemoryKookkieSessionsRepository()
        app = main(config=TestConfig, kookkie_session_repository=self.kookkie_session_repo, kook_repository=self.kook_repository, metricsCollectorCreator=MetricsCollectorCreator.forTest())
        self.client = app.test_client()
        self.smtp_server.start()
        yield
        self.smtp_server.stop()

    def test_can_login_after_resetting_password(self):
        response = self.client.get('/api/resetpassword/{}'.format(str(aValidID('222'))))
        assert_ok(response)
        response = self.client.post('/api/resetpassword', data=json.dumps(dict(new_password='new-password', new_password_confirm='new-password', token=str(aValidID('222')))), content_type='application/json')
        assert_ok(response)
        response_login = self.client.post('/api/login', data=json.dumps(dict(username='henk@qwan.eu', password='new-password')), content_type='application/json')
        assert_ok(response_login)

    def test_request_password_reset(self):
        self.client.post('/api/request-password-reset', data=json_dumps(dict(username='henk@qwan.eu')), content_type='application/json')
        probe_that(lambda: assert_that(self.smtp_server.messages[0], contains_string('henk@qwan.eu')))
        assert_that(self.kook_repository.by_username('henk@qwan.eu').password_reset_token, is_not(self.token))


class TestE2EVersion:
    @pytest.fixture(autouse=True)
    def setup(self):
        app = main(config=TestConfig, kookkie_session_repository = InMemoryKookkieSessionsRepository(),
                   kook_repository=InMemoryKookRepository.empty(),
                   metricsCollectorCreator=MetricsCollectorCreator.forTest())
        self.client = app.test_client()

    def test_returns_version(self):
        with open('VERSION') as f:
            expected_version = f.read().strip()

        response = self.client.get('/api/version', content_type='application/json')
        assert_ok(response)
        assert_that(json.loads(response.data), equal_to(dict(version=expected_version)))


class TestE2EProfile:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.kook_repository = InMemoryKookRepository([
            aValidKook(id=aValidID('445'), name='Henk', email='henk@qwan.eu',
                       hashed_password=PasswordHasher().hash('password'))])
        app = main(config=TestConfig,
                   kookkie_session_repository=InMemoryKookkieSessionsRepository(),
                   kook_repository=self.kook_repository,
                   metricsCollectorCreator=MetricsCollectorCreator.forTest())
        self.client = app.test_client()

    def test_returns_ok_when_not_logged_in(self):
        response = self.client.get('/api/profile', content_type='application/json')
        assert_ok(response)
        
    def test_returns_profile_when_logged_in(self):
        self.client.post('/api/login', data=json.dumps(dict(username='henk@qwan.eu', password='password')), content_type='application/json')
        response = self.client.get('/api/profile', content_type='application/json')
        assert_ok(response)
        assert_that(json.loads(response.data), equal_to(dict(name='Henk', email='henk@qwan.eu', role='kook')))


def csrf_headers(client):
    csrf_token = get_csrf_token(client)
    assert csrf_token is not None
    return {TestConfig.WTF_CSRF_HEADERS[0]: csrf_token.value}


def assert_ok(response):
    assert_that(response.status, equal_to('200 OK'))


def assert_no_content(response):
    assert_that(response.status, equal_to('204 NO CONTENT'))


def assert_created(response):
    assert_that(response.status, equal_to("201 CREATED"))


def assert_401(response):
    assert_that(response.status, equal_to('401 UNAUTHORIZED'))
