from abc import ABC, abstractmethod
from typing import Optional

from app.domain import Kook


class CurrentUserRepository(ABC):
    @abstractmethod
    def current_user(self) -> Optional[Kook]:
        pass


class StubbedCurrentUserRepository(CurrentUserRepository):
    def __init__(self, user: Optional[Kook]):
        self.user = user

    def current_user(self):
        return self.user
