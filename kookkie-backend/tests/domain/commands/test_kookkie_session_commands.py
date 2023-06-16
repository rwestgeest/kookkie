from quiltz.domain.results import PartialSuccess

from app.adapters.repositories import InMemoryKookkieSessionsRepository
from testing import *
from quiltz.domain.id import FixedIDGeneratorGenerating
from app.domain.commands import *
from domain.builders import *
from app.domain import DummyContext
from support.log_collector import log_collector


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


class FixedMessengerFactoryCreating:
    def __init__(self, messenger):
        self.messenger = messenger

    def create(self, context):
        return self.messenger


class TestJoinSession:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = Mock(KookkieSessionsRepository)
        self.join_session = JoinSession(self.repository)

    def test_responds_with_error_when_session_not_found(self):
        self.repository.by_id_with_result.return_value = Failure(message='kookkie session not found')
        assert self.join_session(aValidID(11), aValidID(22)) == Failure(message='kookkie session not found')
    
    def test_joins_to_found_session(self):
        kookkie_session = aValidKookkieSession(id=aValidID('11'), participants=[])
        self.repository.by_id_with_result.return_value = Success(kookkie_session=kookkie_session)
        assert self.join_session(aValidID(11), aValidID(22)) == kookkie_session.join_participant_by_id(aValidID(22))


class TestCloseSession:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = Mock(KookkieSessionsRepository)
        self.repository.by_id_with_result.return_value = Success(kookkie_session=aValidKookkieSession(id=aValidID('456')).open())
        self.close_session = CloseSession(self.repository)
        
    def test_closes_an_open_session(self):
        assert_that(self.close_session(aValidID('456'), aValidKook()).is_success(), equal_to(True))
        self.repository.save.assert_any_call(event=KookkieSessionWasClosed(aValidKookkieSession(id=aValidID('456')).closed()))
        self.repository.by_id_with_result.assert_called_once_with(aValidID('456'), aValidKook())

    def test_does_not_save_when_session_does_not_exist(self):
        self.repository.by_id_with_result.return_value = Failure(message='kookkie session not found')
        assert_that(self.close_session(aValidID(''), aValidKook()),
                    equal_to(Failure(message='kookkie session not found')))
        self.repository.save.assert_not_called()

    def test_resets_participants_email_addresses(self):
        self.close_session(aValidID('456'), aValidKook())
        self.repository.save.assert_any_call(event=ParticipantEmailAddressesWereReset(
            kookkie_session=aValidKookkieSession(id=aValidID('456')).closed()))


class TestOpenSession:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = Mock(KookkieSessionsRepository)
        self.repository.by_id_with_result.return_value = Success(kookkie_session=aValidKookkieSession(id=aValidID('456')))
        self.open_session = OpenSession(self.repository)

    def test_opens_a_closed_session(self):
        assert_that(self.open_session(aValidID('456'), aValidKook()).is_success(), equal_to(True))
        self.repository.save.assert_called_once_with(event=KookkieSessionWasOpened(aValidKookkieSession(id=aValidID('456')).open()))
        self.repository.by_id_with_result.assert_called_once_with(aValidID('456'), aValidKook())

    def test_does_not_save_when_session_does_not_exist(self):
        self.repository.by_id_with_result.return_value = Failure(message='kookkie session not found')
        assert_that(self.open_session(aValidID(''), aValidKook()),
                    equal_to(Failure(message='kookkie session not found')))
        self.repository.save.assert_not_called()



class TestAddParticipant:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.id_generator = FixedIDGeneratorGenerating(aValidID('88'))
        self.repository = Mock(KookkieSessionsRepository)
        self.kookkie_session = aValidKookkieSession(id=aValidID('456'))
        self.repository.by_id_with_result.return_value = Success(kookkie_session=self.kookkie_session)
        self.add_participant = AddParticipant(kookkie_session_repository=self.repository,
                                              id_generator=self.id_generator)

    def test_adds_a_participant(self):
        result = self.add_participant(aValidID('456'), aValidKook())
        assert_that(result.is_success(), equal_to(True))
        self.repository.save.assert_called_once_with(
            self.kookkie_session.add_participant(self.id_generator).event)

    def test_returns_failure_if_adding_fails(self):
        kookkie_session = aValidKookkieSession(id=aValidID('456'), participants=[aValidKookkieParticipant() for i in range(30)])
        self.repository.by_id_with_result.return_value = Success(kookkie_session=kookkie_session)
        result = self.add_participant(aValidID('456'), aValidKook())
        assert_that(result.is_success(), equal_to(False))
        self.repository.save.assert_not_called()


class TestSetParticipantEmailAddresses:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = Mock(KookkieSessionsRepository)
        self.kookkie_session = aValidKookkieSession(id=aValidID('456'), participants=[aValidKookkieParticipant(id=aValidID(55), email='')])
        self.repository.by_id_with_result.return_value = Success(kookkie_session=self.kookkie_session)
        self.set_participant_email_addresses = SetParticipantEmailAddresses(kookkie_session_repository=self.repository)

    def test_sets_email_addresses(self):
        email_data = dict(email_addresses=[dict(email='henk@mail.com', participant_id=str(aValidID('55')))])
        result = self.set_participant_email_addresses(aValidID('456'), email_data)
        assert_that(result, equal_to(Success()))
        self.repository.save.assert_called_once_with(
            self.kookkie_session.set_participant_email_addresses(EmailAddresses.from_data(email_data)).event)

    def test_returns_failure_if_setting_fails(self):
        email_data = dict(email_addresses=[dict(email='henk@mail.com', participant_id=str(aValidID('1')))])
        result = self.set_participant_email_addresses(aValidID('456'), email_data)
        assert_that(result, equal_to(Failure(message='Invalid participant id: {}'.format(str(aValidID('1'))))))
        self.repository.save.assert_not_called()
