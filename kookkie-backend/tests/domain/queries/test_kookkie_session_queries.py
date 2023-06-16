from testing import *
from app.domain.queries import GetKookkieSessionQuery
from app.domain.repositories import InMemoryKookRepository
from domain.builders import *


class TestGetKookkieSessionQuery:
    @pytest.fixture(autouse=True)  
    def setup(self):
        self.kookkie_sessions_repo = Mock()
        self.kook_repo = Mock()
        self.query = GetKookkieSessionQuery(self.kookkie_sessions_repo, self.kook_repo)

    def test_returns_failure_when_session_not_found(self):
        self.kookkie_sessions_repo.by_id_with_result.return_value = Failure(message='unknown kookkie session')
        assert_that(self.query(aValidID(23), aValidKook()), equal_to(Failure(message='unknown kookkie session')))

    def test_returns_the_session(self):
        self.kookkie_sessions_repo.by_id_with_result.return_value = Success(kookkie_session=aValidKookkieSession())
        assert_that(self.query(aValidID(23), aValidKook()), equal_to(Success(kookkie_session=aValidKookkieSession())))
        self.kookkie_sessions_repo.by_id_with_result.assert_called_once_with(aValidID(23), aValidKook())

