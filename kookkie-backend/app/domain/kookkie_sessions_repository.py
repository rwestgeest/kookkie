from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Iterable, List
from quiltz.domain import ID
from quiltz.domain.results import Result

from app.domain import KookkieSessionEvent, KookkieSessionListItem
from app.domain import Kook


class KookkieSessionsRepository(ABC):
    @abstractmethod
    def all(self, kook: Kook) -> List[KookkieSessionListItem]:
        pass
        
    @abstractmethod
    def by_id_with_result(self, kookkie_session_id: ID, kook: Kook) -> Result:
        pass

    @abstractmethod
    def save_all(self, events: list[KookkieSessionEvent]):
        pass

    @abstractmethod
    def save(self, event: KookkieSessionEvent):
        pass