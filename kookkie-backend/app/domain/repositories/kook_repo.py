from abc import abstractmethod, ABC
from typing import Optional

from quiltz.domain import ID, Failure
from quiltz.domain.results import Result

from app.domain import PasswordResetToken, Kook


FACILITATOR_NOT_FOUND = Failure(message="kook not found")


class KookRepository(ABC):
    def with_admins(self) -> 'KookRepository':
        return self

    def repair(self) -> 'KookRepository':
        return self

    @abstractmethod
    def has_user(self, username: str) -> bool: pass

    @abstractmethod
    def by_username(self, username: str) -> Optional[Kook]: pass

    @abstractmethod
    def by_username_with_result(self, username: str) -> Result: pass

    @abstractmethod
    def by_id_with_result(self, id: ID) -> Result: pass

    @abstractmethod
    def by_token(self, token: PasswordResetToken) -> Optional[Kook]: pass

    @abstractmethod
    def all(self) -> list[Kook]: pass

    @abstractmethod
    def save(self, kook: Kook): pass

    @abstractmethod
    def remove(self, id: ID): pass
