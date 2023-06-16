import pytest
from .db_kookkie_sessions_repository_test import DbKookkieSessionsRepositoryTest
from hamcrest import assert_that, equal_to
from app.adapters.repositories import InMemoryKookkieSessionsRepository, hard_coded_sessions, \
    KOOKKIE_SESSION_NOT_FOUND, admins
from domain.builders import *
from app.domain import (
    KookkieSessionWasClosed,
    KookkieSessionWasOpened)


class TestInMemoryKookkieSessionsRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = InMemoryKookkieSessionsRepository()
        self.kook = aValidKook()
        self.kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(kook_id=self.kook.id))
    
    def test_an_empty_kookkie_session_repo_has_no_items(self):
        assert self.repo.all(aValidKook()) == []

    def test_creating_a_kookkie_session_makes_it_available_in_the_repo(self):
        self.repo.save(event=self.kookkie_session_created)
        assert self.repo.all(aValidKook()) == [self.kookkie_session_created.kookkie_session.as_list_item()]

    def test_all_returns_only_accessible_sessions(self):
        other_kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('999'), kook_id=aValidID('888')))
        self.repo.save(event=other_kookkie_session_created)
        assert self.repo.all(aValidKook()) == []

    def test_all_returns_sessions_sorted_ascending_by_date(self):
        session_1 = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('71'), date='2020-02-10'))
        session_2 = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('72'), date='2020-01-01'))
        self.repo.save_all(events=[session_1, session_2])
        assert_that(self.repo.all(aValidKook()),
                    equal_to([session_2.kookkie_session.as_list_item(), session_1.kookkie_session.as_list_item()]))

    def test_kookkie_sessions_are_available_by_id(self):
        self.repo.save(event=self.kookkie_session_created)
        assert_that(self.repo._by_id(self.kookkie_session_created.id, self.kook),
                    equal_to(self.kookkie_session_created.kookkie_session))

    def test_by_id_returns_none_when_kookkie_session_is_not_available(self):
        assert self.repo._by_id(aValidID('1'), self.kook) is None

    def test_by_id_returns_none_when_kook_does_not_have_access(self):
        self.repo.save(event=self.kookkie_session_created)
        assert self.repo._by_id(aValidID('1'), aValidKook(id=aValidID('200'))) is None

    def test_by_id_returns_session_when_kook_is_not_known(self):
        self.repo.save(event=self.kookkie_session_created)
        assert_that(self.repo._by_id(aValidID('1'), None), equal_to(self.kookkie_session_created.kookkie_session))


class TestInMemoryKookkieSessionsRepository_by_id_with_result:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = InMemoryKookkieSessionsRepository()
        self.kook = aValidKook()
        self.kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(kook_id=self.kook.id))

    def test_is_failure_when_not_found(self):
        assert_that(self.repo.by_id_with_result(aValidID(23), self.kook),
                    equal_to(KOOKKIE_SESSION_NOT_FOUND))

    def test_is_success_when_found(self):
        self.repo.save(event=self.kookkie_session_created)
        assert_that(self.repo.by_id_with_result(self.kookkie_session_created.id, self.kook),
                    equal_to(Success(kookkie_session=self.kookkie_session_created.kookkie_session)))


class TestInMemoryKookkieSessionsRepositorySaveDeleted:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = InMemoryKookkieSessionsRepository()

    def test_kookkie_session_was_deleted_deletes_the_session(self):
        kookkie_session = aValidKookkieSession(id=aValidID('55'),
                                                     participants=[aValidKookkieParticipant(id=aValidID('90'))])
        another_session = aValidKookkieSession(id=aValidID('54'),
                                                  participants=[aValidKookkieParticipant(id=aValidID('92'))])
        self.repo.save(aValidKookkieSessionCreatedEvent(kookkie_session=kookkie_session))
        self.repo.save(aValidKookkieSessionCreatedEvent(kookkie_session=another_session))
        self.repo.save(KookkieSessionWasDeleted(kookkie_session))
        assert_that(self.repo.by_id_with_result(kookkie_session.id, kook=aValidKook()),
                    equal_to(KOOKKIE_SESSION_NOT_FOUND))


class TestInMemoryKookkieSessionsRepositoryWithHardcodedValues:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = InMemoryKookkieSessionsRepository.with_hard_coded_values()
        
    def test_all_return_all_kookkie_sessions_in_the_repository(self):
        assert_that(self.repo.all(aValidKook(id=admins[0].id)), equal_to([s.as_list_item() for s in hard_coded_sessions]))


class TestDbKookkieSessionsRepositorySaveCreated(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        with self.a_db_with():  # nothing
            yield

    def test_an_empty_kookkie_session_repo_has_no_items(self):
        assert self.repo.all(aValidKook()) == []

    def test_creating_a_kookkie_session_makes_it_available_in_the_repo(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('999'), kook_id=aValidKook().id))
        self.repo.save(event=kookkie_session_created)
        assert_that(self.repo.all(aValidKook()), equal_to([kookkie_session_created.kookkie_session.as_list_item()]))

    def test_all_returns_only_accessible_sessions(self):
        other_kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('999'), kook_id=aValidID('888')))
        self.repo.save(event=other_kookkie_session_created)
        assert_that(self.repo.all(aValidKook()), equal_to([]))

    def test_all_returns_sessions_sorted_ascending_by_date(self):
        session_1 = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('71'), date='2020-02-10'))
        session_2 = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(id=aValidID('72'), date='2020-01-01'))
        self.repo.save_all(events=[session_1, session_2])
        assert_that(self.repo.all(aValidKook()),
                    equal_to([session_2.kookkie_session.as_list_item(),
                              session_1.kookkie_session.as_list_item()]))

    def test_kookkie_sessions_are_available_by_id(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent()
        self.repo.save(event=kookkie_session_created)
        assert_that(self.repo._by_id(kookkie_session_created.id, aValidKook()),
                    equal_to(kookkie_session_created.kookkie_session))

    def test_by_id_with_kook_returns_none_when_kookkie_session_is_not_available(self):
        assert self.repo._by_id(aValidID('1'), aValidKook()) is None

    def test_by_id_returns_none_when_kook_does_not_have_access(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent()
        self.repo.save(event=kookkie_session_created)
        assert self.repo._by_id(aValidID('1'), aValidKook(id=aValidID('200'))) is None

    def test_by_id_returns_none_when_kookkie_session_is_not_available(self):
        assert self.repo._by_id(aValidID('1')) is None

    def test_reads_all_attributes_of_a_session_from_the_repo(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent(kookkie_session=aValidKookkieSession())
        self.repo.save(event=kookkie_session_created)
        session = self.repo._by_id(kookkie_session_created.id)
        assert session == kookkie_session_created.kookkie_session

    def test_by_id_returns_session_when_kook_is_not_known(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent()
        self.repo.save(event=kookkie_session_created)
        assert self.repo._by_id(aValidID('1'), None) == kookkie_session_created.kookkie_session

    def test_reads_a_participant_of_a_session_from_the_repo(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session = aValidKookkieSession(participants=[
                aValidKookkieParticipant(email='participant@qwan.eu')
            ])
        )
        self.repo.save(event=kookkie_session_created)
        assert_that(self.repo._by_id(kookkie_session_created.id, kook=aValidKook()),
                    equal_to(kookkie_session_created.kookkie_session))

    def test_reads_more_participant_of_a_session_from_the_repo(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session = aValidKookkieSession(participants=[
                aValidKookkieParticipant(id=aValidID(5656)),
                aValidKookkieParticipant(id=aValidID(6767))
            ])
        )
        self.repo.save(event=kookkie_session_created)
        assert_that(self.repo._by_id(kookkie_session_created.id, kook=aValidKook()),
                    equal_to(kookkie_session_created.kookkie_session))

    def test_reads_default_participant_values_for_email(self):
        kookkie_session_created = aValidKookkieSessionCreatedEvent(
            kookkie_session=aValidKookkieSession(participants=[
                aValidKookkieParticipant(email=None)
            ])
        )
        self.repo.save(event=kookkie_session_created)
        assert_that(self.repo._by_id(kookkie_session_created.id, kook=aValidKook()),
                    equal_to(aValidKookkieSession(participants=[
                        aValidKookkieParticipant(email='')
                    ])))


class TestDbKookkieSessionsRepository_by_id_with_result(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        with self.a_db_with(): # nothing
            self.kook = aValidKook()
            self.kookkie_session_created = aValidKookkieSessionCreatedEvent(
                kookkie_session=aValidKookkieSession(kook_id=self.kook.id))
            yield

    def test_is_failure_when_not_found(self):
        assert_that(self.repo.by_id_with_result(aValidID(23), self.kook), equal_to(KOOKKIE_SESSION_NOT_FOUND))

    def test_is_success_when_found(self):
        self.repo.save(event=self.kookkie_session_created)
        assert_that(self.repo.by_id_with_result(self.kookkie_session_created.id, self.kook), equal_to(Success(kookkie_session=self.kookkie_session_created.kookkie_session)))


class TestDbKookkieSessionsRepositorySaveDeleted(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        self.kookkie_session = aValidKookkieSession(id=aValidID('55'),
                                                          participants=[aValidKookkieParticipant(id=aValidID('90'))])
        self.another_session = aValidKookkieSession(id=aValidID('54'),
                                                       participants=[aValidKookkieParticipant(id=aValidID('92'))])
        with self.a_db_with(self.kookkie_session, self.another_session):
            yield

    def test_kookkie_session_was_deleted_does_not_delete_anything_else(self):
        self.repo.save(event=KookkieSessionWasDeleted(self.kookkie_session))
        assert_that(self.repo.by_id_with_result(self.another_session.id, kook=aValidKook()),
                    equal_to(Success(kookkie_session=self.another_session)))


class TestDbKookkieSessionsRepositorySaveOpenedAndClosed(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        self.kookkie_session = aValidKookkieSession(participants=[
            aValidKookkieParticipant(id=aValidID(5656)),
            aValidKookkieParticipant(id=aValidID(6767))
        ])
        with self.a_db_with(self.kookkie_session):
            yield

    def test_kookkie_session_was_opened_opens_the_session(self):
        self.repo.save(event=KookkieSessionWasOpened(self.kookkie_session))
        assert_that(self.repo._by_id(self.kookkie_session.id, kook=aValidKook()).is_open,
                    equal_to(True))

    def test_kookkie_session_was_closed_closes_the_session(self):
        self.repo.save(event=KookkieSessionWasOpened(self.kookkie_session))
        self.repo.save(event=KookkieSessionWasClosed(self.kookkie_session))
        assert_that(self.repo._by_id(self.kookkie_session.id, kook=aValidKook()).is_open,
                    equal_to(False))


class TestDbKookkieSessionsRepositorySaveParticipantWasAdded(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        self.kookkie_session = aValidKookkieSession()
        with self.a_db_with(self.kookkie_session):
            yield

    def test_participant_was_added_adds_new_participant_to_the_session(self):
        new_participant = KookkieParticipant(id=aValidID('40'), joining_id=aValidID('50'))
        self.repo.save(event=ParticipantWasAdded(self.kookkie_session,
                                                 new_participant=new_participant))
        result = self.repo._by_id(self.kookkie_session.id, kook=aValidKook())
        assert_that(result.participant_count(), equal_to(1))
        assert_that(result.participants[0], equal_to(new_participant)) 


class TestDbKookkieSessionsRepositorySaveParticipantEmailAddressesWereReset(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        self.kookkie_session = aValidKookkieSession(participants=[aValidKookkieParticipant(id=aValidID('40'), email='john@mail.com'),
                                                                        aValidKookkieParticipant(id=aValidID('41'), email='dirk@mail.com')])
        with self.a_db_with(self.kookkie_session):
            yield

    def test_saves_participant_email_addresses(self):
        self.repo.save(ParticipantEmailAddressesWereReset(kookkie_session=self.kookkie_session))
        result = self.repo._by_id(self.kookkie_session.id, kook=aValidKook())
        assert_that(result._participant_by_id(aValidID('40')).email, equal_to(''))
        assert_that(result._participant_by_id(aValidID('41')).email, equal_to(''))


class TestDbKookkieSessionsRepositorySaveParticipantEmailAddressesWereSet(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_db(self):
        self.kookkie_session = aValidKookkieSession(participants=[aValidKookkieParticipant(id=aValidID('40'), email=''),
                                                                        aValidKookkieParticipant(id=aValidID('41'), email='dirk@mail.com')])
        with self.a_db_with(self.kookkie_session):
            yield

    def test_saves_participant_email_addresses(self):
        self.repo.save(ParticipantEmailAddressesWereSet(kookkie_session=self.kookkie_session, email_addresses=[EmailAddress(participant_id=aValidID('40'), email='john@mail.com')]))
        result = self.repo._by_id(self.kookkie_session.id, kook=aValidKook())
        assert_that(result._participant_by_id(aValidID('40')).email, equal_to('john@mail.com'))
        assert_that(result._participant_by_id(aValidID('41')).email, equal_to('dirk@mail.com'))

    def test_saves_empty_participant_email_addresses(self):
        self.repo.save(ParticipantEmailAddressesWereSet(kookkie_session=self.kookkie_session, email_addresses=[EmailAddress(participant_id=aValidID('41'), email='')]))
        result = self.repo._by_id(self.kookkie_session.id, kook=aValidKook())
        assert_that(result._participant_by_id(aValidID('41')).email, equal_to(''))
