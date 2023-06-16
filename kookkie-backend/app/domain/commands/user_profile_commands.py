from app.domain import Clock
from app.domain.kook import Kook
from app.domain.repositories import KookRepository
from app.domain.messenger import MessengerFactory
from app.domain.password_hasher import PasswordHasher
from quiltz.domain.anonymizer import anonymize
from quiltz.domain.results import Failure, Success, Result
import logging


class AcceptTermsOfService:
    def __init__(self, clock: Clock, user_repository: KookRepository):
        self.clock = clock
        self.user_repository = user_repository

    def __call__(self, current_user: Kook, version: str, accepted: bool) -> Result:
        if version != '2023.1':
            return Failure(message='Wrong Terms of Service version {}'.format(version))
        updated = current_user.accept(self.clock, version)
        self.user_repository.save(updated)
        return Success()
