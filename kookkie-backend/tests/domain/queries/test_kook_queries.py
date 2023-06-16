from quiltz.domain.id.testbuilders import aValidID
from testing import *
from domain.builders import aValidKook, aValidAdministrator
from app.domain.queries import AllKooks, AllKookSessionCounts
from app.domain import Success, Failure, Clock, KookSessionCounts, KookSessionCount
from app.domain.repositories import InMemoryKookRepository


def names_of(kook):
    return list(map(lambda f: f.name, kook))


class TestAllKooksQuery:
    def test_returns_all_kook(self):
        kook_repo = InMemoryKookRepository([aValidKook()])
        query = AllKooks(kook_repo)
        assert_that(query(aValidAdministrator()), equal_to(Success(kooks=[aValidKook()])))

    def test_fails_for_non_admin_user(self):
        query = AllKooks(None)
        assert_that(query(aValidKook()), equal_to(Failure(message='not allowed to view kooks')))

    def test_sorts_by_name(self):
        kook_repo = InMemoryKookRepository.empty()
        kook_repo.save(aValidKook(id=aValidID('11'), name='John'))
        kook_repo.save(aValidKook(id=aValidID('12'), name='Alex'))
        query = AllKooks(kook_repo)
        assert_that(names_of(query(aValidAdministrator()).kooks), equal_to(['Alex', 'John']))
    

class TestAllKookCountsQuery:
    def test_returns_all_counts(self):
        kookkie_session_repo = Mock()
        counts = KookSessionCounts(KookSessionCount(id=aValidID(1), name='Henk', count=1))
        kookkie_session_repo.count_kookkies_by_kooks.return_value = counts
        query = AllKookSessionCounts(kookkie_session_repo)
        assert_that(query(aValidAdministrator()), equal_to(Success(counts=counts)))

    def test_passes_since_parameter_to_query(self):
        kookkie_session_repo = Mock()
        counts = KookSessionCounts(KookSessionCount(id=aValidID(1), name='Henk', count=1))
        kookkie_session_repo.count_kookkies_by_kooks.return_value = counts
        query = AllKookSessionCounts(kookkie_session_repo)
        query(aValidAdministrator(), since=Clock.fixed().now())
        kookkie_session_repo.count_kookkies_by_kooks.assert_called_once_with(since=Clock.fixed().now())
    
    def test_fails_for_non_admin_user(self):
        query = AllKookSessionCounts(None)
        assert_that(query(aValidKook()), equal_to(Failure(message='not allowed to view kook counts')))
