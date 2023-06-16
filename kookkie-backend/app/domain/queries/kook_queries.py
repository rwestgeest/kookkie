from datetime import datetime
from typing import Optional

from app.domain import Success, Failure, Kook


class AllKooks():
    def __init__(self, kook_repository):
        self.kook_repository = kook_repository

    def __call__(self, user=None):
        if user and not user.is_admin:
            return Failure(message='not allowed to view kooks')
        return Success(kooks=sorted(self.kook_repository.all(), key=lambda f: f.name))


class AllKookSessionCounts:
    def __init__(self, kookkie_session_repository):
        self.kookkie_session_repository = kookkie_session_repository

    def __call__(self, user: Kook, since: Optional[datetime] = None):
        if not user.is_admin:
            return Failure(message='not allowed to view kook counts')
        counts = self.kookkie_session_repository.count_kookkies_by_kooks(since=since)
        return Success(counts=counts)
