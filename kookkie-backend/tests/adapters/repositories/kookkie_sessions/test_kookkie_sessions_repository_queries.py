import pytest
from .db_kookkie_sessions_repository_test import DbKookkieSessionsRepositoryTest
from hamcrest import assert_that, equal_to
from app.adapters.repositories import InMemoryKookkieSessionsRepository, DBKookkieSessionsRepository
from domain.builders import *
from app.domain import KookkieSessionCreated, KookSessionCount, Clock
from datetime import timedelta

class TestInMemoryKookkieSessionsRepositorySessionCounts:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.repo = InMemoryKookkieSessionsRepository()
        self.kook = aValidKook()
        
    def test_an_empty_kookkie_session_repo_has_no_items(self):
        assert_that(self.repo.count_sessions_by_kooks(), equal_to(KookSessionCounts()))

    def test_counts_sessions_by_kook(self):
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(1)))
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(2)))
        self.repo.save(sessionCreatedFor(aValidKook(name='Harrie', id=aValidID(2)), id=aValidID(3)))
        assert_that(self.repo.count_sessions_by_kooks(), equal_to(KookSessionCounts(
            KookSessionCount(name='Henk',id=aValidID(1), count=2),
            KookSessionCount(name='Harrie', id=aValidID(2), count=1))))

    def test_ignores_since_parameter(self):
        now = timestamp=Clock().now()
        an_hour_ago = now - timedelta(hours=1)
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(1), timestamp=now))
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(2), timestamp=an_hour_ago))
        assert_that(self.repo.count_sessions_by_kooks(since=now), equal_to(KookSessionCounts(
            KookSessionCount(name='Henk',id=aValidID(1), count=2))))


class TestDbKookkieSessionsRepositorySessionCounts(DbKookkieSessionsRepositoryTest):
    __test__ = True

    @pytest.fixture(autouse=True)
    def setupDb(self):            
        with self.a_db_with(): # nothing
            yield

    def test_an_empty_kookkie_session_repo_has_no_items(self):
        assert_that(self.repo.count_sessions_by_kooks(), equal_to(KookSessionCounts()))

    def test_counts_sessions_by_kook(self):
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(1)))
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(2)))
        self.repo.save(sessionCreatedFor(aValidKook(name='Harrie', id=aValidID(2)), id=aValidID(3)))
        assert_that(self.repo.count_sessions_by_kooks(), equal_to(KookSessionCounts(
            KookSessionCount(name='Henk',id=aValidID(1), count=2),
            KookSessionCount(name='Harrie', id=aValidID(2), count=1))))

    def test_counts_sessions_by_kook_since_some_timestamp(self):
        now = timestamp = Clock().now()
        an_hour_ago = now - timedelta(hours=1)
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(1), timestamp=now))
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(2), timestamp=an_hour_ago))
        self.repo.save(sessionCreatedFor(aValidKook(name='Henk', id=aValidID(1)), id=aValidID(3), timestamp=an_hour_ago - timedelta(hours=1)))
        assert_that(self.repo.count_sessions_by_kooks(since=an_hour_ago), equal_to(KookSessionCounts(
            KookSessionCount(name='Henk',id=aValidID(1), count=2))))


def sessionCreatedFor(kook, id, timestamp=None):
    if timestamp is None: timestamp = Clock().now() - timedelta(weeks=1)
    return KookkieSessionCreated(aValidKookkieSession(id=id, kook_id=kook.id, kook_name=kook.name), timestamp=timestamp)