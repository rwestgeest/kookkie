from quiltz.domain import Success, ID

from app.domain import Kook, PasswordResetToken
from app.domain.repositories import KookRepository
from domain.builders import aValidKook


class StubbedKookRepository(KookRepository):
    def by_username(self, username: str):
        return aValidKook()

    def by_id_with_result(self, id: ID):
        return Success(kook=aValidKook())

    def has_user(self, username): pass
    def by_username_with_result(self, username: str): pass
    def by_token(self, token: PasswordResetToken): pass
    def all(self): pass
    def save(self, kook: Kook): pass
    def remove(self, id: ID): pass
