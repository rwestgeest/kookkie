from typing import Optional

from quiltz.domain import Success, ID
from quiltz.domain.results import Result

from app.domain import Kook, PasswordResetToken
from app.domain.repositories.kook_repo import KookRepository, FACILITATOR_NOT_FOUND


class InMemoryKookRepository(KookRepository):
    @staticmethod
    def empty() -> "InMemoryKookRepository":
        return InMemoryKookRepository(users=[])

    def __init__(self, users: list[Kook]):
        self._users = {user.id: user for user in users}

    def has_user(self, username: str) -> bool:
        return self.by_username(username) is not None

    def by_username(self, username: str) -> Optional[Kook]:
        return next((user for user in self.all() if user.username.lower() == username.lower()), None)

    def by_username_with_result(self, username: str) -> Result:
        kook = self.by_username(username)
        return Success(kook=kook) if kook else FACILITATOR_NOT_FOUND

    def _by_id(self, id: ID) -> Optional[Kook]:
        return self._users.get(id)

    def by_id_with_result(self, id: ID) -> Result:
        kook = self._by_id(id)
        return Success(kook=kook) if kook else FACILITATOR_NOT_FOUND

    def by_token(self, token: PasswordResetToken) -> Optional[Kook]:
        return next((user for user in self.all() if token.is_within_expiry_of(user.password_reset_token)), None)

    def all(self) -> list[Kook]:
        return list(self._users.values())

    def save(self, kook: Kook):
        self._users[kook.id] = kook

    def remove(self, id: ID):
        del self._users[id]
