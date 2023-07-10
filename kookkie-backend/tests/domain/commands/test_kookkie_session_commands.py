from quiltz.domain.id import FixedIDGeneratorGenerating

from app.domain.commands import *
from domain.builders import *
from domain.repair.fake_jaas_jwt_builder import FakeJaasJwtBuilder
from testing import *


class TestCreateKookkieSession:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = Mock(KookkieSessionsRepository)
        self.id_generator = FixedIDGeneratorGenerating(aValidID(12))
        self.clock = Clock.fixed()
        self.create_kookkie_session = CreateKookkieSession(
            kookkie_session_repository=self.repo,
            id_generator=self.id_generator, 
            clock=self.clock)
        
    def test_saves_a_new_kookkie_session_with_an_id_in_the_repo(self):
        session_creator = KookkieSessionCreator(id_generator=self.id_generator, clock=self.clock)
        self.create_kookkie_session(validKookkieSessionCreationParameters())
        expected_event = session_creator.create_with_id(**validKookkieSessionCreationParameters()).kookkie_session_created
        self.repo.save.assert_called_once_with(event=expected_event)
            
    def test_returns_success_if_all_ok(self):
        result = self.create_kookkie_session(validKookkieSessionCreationParameters())
        assert result == Success(id = aValidID('12'))

    def test_returns_failure_if_something_failed(self):
        result = self.create_kookkie_session(dict())
        assert result == Failure(message='failed to create kookkie session')


class TestStartKookkieSession:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = Mock(KookkieSessionsRepository)
        self.jwt_builder = FakeJaasJwtBuilder()
        self.start_kookkie_session = StartKookkieSession(
            kookkie_session_repository=self.repo,
            jaas_jwt_builder=self.jwt_builder
        )

    def test_creates_joining_info_with_kookkie_and_jwt(self):
        kookkie_session = aValidKookkieSession()
        self.repo.by_id_with_result.return_value = Success(kookkie_session=kookkie_session)
        result = self.start_kookkie_session(kookkie_id=aValidID("12"), kook=aValidKook())
        assert_that(result, equal_to(kookkie_session.start(aValidKook(), self.jwt_builder)))

    def test_returns_not_found_when_kookkie_session_does_not_exist(self):
        self.repo.by_id_with_result.return_value = Failure(message="not found")
        result = self.start_kookkie_session(kookkie_id=aValidID("12"), kook=aValidKook())
        assert_that(result, equal_to(Failure(message="not found")))

class FixedMessengerFactoryCreating:
    def __init__(self, messenger):
        self.messenger = messenger

    def create(self, context):
        return self.messenger


class TestJoinSession:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = Mock(KookkieSessionsRepository)
        self.jwt_builder = FakeJaasJwtBuilder()
        self.join_session = JoinSession(self.repository, self.jwt_builder)

    def test_responds_with_error_when_session_not_found(self):
        self.repository.by_id_with_result.return_value = Failure(message='kookkie session not found')
        assert self.join_session(aValidID(11)) == Failure(message='kookkie session not found')
    
    def test_creates_joining_info_with_kookkie_and_jwt(self):
        kookkie_session = aValidKookkieSession()
        self.repository.by_id_with_result.return_value = Success(kookkie_session=kookkie_session)
        result = self.join_session(kookkie_session_id=aValidID("12"), name="harry")
        assert_that(result, equal_to(kookkie_session.join("harry", self.jwt_builder)))

