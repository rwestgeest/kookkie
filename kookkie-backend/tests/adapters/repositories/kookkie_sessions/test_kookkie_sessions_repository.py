import pytest
from .db_kookkie_sessions_repository_test import DbKookkieSessionsRepositoryTest
from hamcrest import assert_that, equal_to
from app.adapters.repositories import InMemoryKookkieSessionsRepository, hard_coded_sessions, \
    KOOKKIE_SESSION_NOT_FOUND, admins
from domain.builders import *


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
        kookkie_session = aValidKookkieSession(id=aValidID('55'))
        another_session = aValidKookkieSession(id=aValidID('54'))
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
        assert_that(self.repo.all(aValidKook(id=admins[0].id)), equal_to([hard_coded_sessions[1].as_list_item()]))


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
        self.kookkie_session = aValidKookkieSession(id=aValidID('55'))
        self.another_session = aValidKookkieSession(id=aValidID('54'))
        with self.a_db_with(self.kookkie_session, self.another_session):
            yield

    def test_kookkie_session_was_deleted_does_not_delete_anything_else(self):
        self.repo.save(event=KookkieSessionWasDeleted(self.kookkie_session))
        assert_that(self.repo.by_id_with_result(self.another_session.id, kook=aValidKook()),
                    equal_to(Success(kookkie_session=self.another_session)))


