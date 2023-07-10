from quiltz.domain import Success
from quiltz.domain.id.testbuilders import aValidID

from app.adapters.metrics import NoMetricsCollector
from testing import *
from app.domain import CountingKookkieSessionRepository, Clock
from domain.builders import aValidKookkieSession, aValidKook, aValidKookkieSessionCreatedEvent


class TestCountingKookkieSessionRepository_Queries:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.wrapped_repo = Mock()
        self.repo = CountingKookkieSessionRepository(self.wrapped_repo, NoMetricsCollector())

    def test_all_delegates_to_repository(self):
        self.wrapped_repo.all.return_value = [aValidKookkieSession()]
        assert_that(self.repo.all(aValidKook()), equal_to([aValidKookkieSession()]))
        self.wrapped_repo.all.assert_called_once_with(aValidKook())

    def test_by_id_with_result_delegates_to_repository(self):
        self.wrapped_repo.by_id_with_result.return_value = Success(kookkie_session=aValidKookkieSession())
        assert_that(self.repo.by_id_with_result(aValidID(12), aValidKook()),
                    equal_to(Success(kookkie_session=aValidKookkieSession())))
        self.wrapped_repo.by_id_with_result.assert_called_once_with(aValidID(12), aValidKook())

    def test_by_id_with_id_skips_kook_if_not_given(self):
        self.repo.by_id_with_result(aValidID(12))
        self.wrapped_repo.by_id_with_result.assert_called_once_with(aValidID(12), None)

    def test_count_sessions_by_kook_delegates_to_repository(self):
        now = Clock().now()
        self.repo.count_sessions_by_kooks(now)
        self.wrapped_repo.count_sessions_by_kooks.assert_called_once_with(now)

    def test_save_delegates_to_repository(self):
        self.repo.save(event=aValidKookkieSessionCreatedEvent())
        self.wrapped_repo.save.assert_called_once_with(event=aValidKookkieSessionCreatedEvent())

    def test_save_all_delegates_to_repository(self):
        self.repo.save_all(events=[aValidKookkieSessionCreatedEvent()])
        self.wrapped_repo.save_all.assert_called_once_with(events=[aValidKookkieSessionCreatedEvent()])


class TestCountingKookkieSessionRepository_Save:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.wrapped_repo = Mock()
        self.metrics_collector = Mock()
        self.repo = CountingKookkieSessionRepository(self.wrapped_repo, self.metrics_collector)

    def test_delegates_to_repository(self):
        self.repo.save(event=aValidKookkieSessionCreatedEvent())
        self.wrapped_repo.save.assert_called_once_with(event=aValidKookkieSessionCreatedEvent())

    def test_collects_the_created_event(self):
        self.repo.save(event=aValidKookkieSessionCreatedEvent())
        self.metrics_collector.collect_event.assert_called_once_with("KookkieSessionCreated")
