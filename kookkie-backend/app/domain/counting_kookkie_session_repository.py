from datetime import datetime
from typing import Optional

from . import KookkieSessionEvent, Kook
from .kookkie_sessions_repository import KookkieSessionsRepository


class CountingKookkieSessionRepository(KookkieSessionsRepository):
    def __init__(self, wrapped_repo, metrics_collector):
        self._wrapped_repo = wrapped_repo
        self._metrics_collector = metrics_collector

    def count_sessions_by_kooks(self, since: Optional[datetime] = None):
        return self._wrapped_repo.count_sessions_by_kooks(since)

    def all(self, kook: Kook):
        return self._wrapped_repo.all(kook)

    def by_id_with_result(self, id, kook=None):
        return self._wrapped_repo.by_id_with_result(id, kook)

    def save(self, event: KookkieSessionEvent):
        self._wrapped_repo.save(event=event)
        self._metrics_collector.collect_event(event.name)

    def save_all(self, events: list[KookkieSessionEvent]):
        self._wrapped_repo.save_all(events=events)
        for event in events:
            self._metrics_collector.collect_event(event.name)
