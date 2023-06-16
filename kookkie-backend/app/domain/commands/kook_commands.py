from typing import Optional, Dict
import logging

from quiltz.domain import ID
from quiltz.domain.id import IDGenerator
from quiltz.domain.anonymizer import anonymize
from quiltz.domain.results import Result

from app.domain import KookCreator, Success, Failure, Kook
from app.domain.repositories import KookRepository
from app.domain.password_reset_token_generator import PasswordResetTokenGenerator


class CreateKook:
    def __init__(self, kook_repository, message_engine, messenger_factory, id_generator=IDGenerator(),
                 password_reset_token_generator=PasswordResetTokenGenerator()):
        self.kook_repository = kook_repository
        self.id_generator = id_generator
        self.password_reset_token_generator = password_reset_token_generator
        self.message_engine = message_engine
        self.messenger_factory = messenger_factory

    def __call__(self, attributes, context, user: Kook) -> Result:
        if not user.is_admin:
            return Failure(message='not allowed to create a kook')

        messenger = self.messenger_factory.create(context=context)

        return (KookCreator(id_generator=self.id_generator)
                .create_with_id(**attributes)
                .map(lambda r: self.check_uniqueness(r.kook))
                .map(lambda r: Success(kook=r.kook.welcome(messenger, self.password_reset_token_generator)))
                .do(lambda r: self.kook_repository.save(r.kook))
                .do(lambda r: self.message_engine.commit(messenger))
                .map(lambda r: Success(id=r.kook.id)))

    def check_uniqueness(self, kook: Kook) -> Result:
        if self.kook_repository.by_username(kook.email) is not None:
            return Failure(message='kook already exists')
        return Success(kook=kook)


def authorize_admin_only(user: Kook, command: str) -> Result:
    return user.is_admin and Success() or Failure(message='not allowed to {what}'.format(what=command))


def cannot_change_yourself(kook_id: ID, user: Kook, what: str) -> Result:
    return kook_id != user.id and Success() or Failure(message='not allowed to {what} yourself'.format(what=what))


class UpdateKookBaseCommand:
    def __init__(self, kook_repository: KookRepository):
        self._kook_repository = kook_repository

    def __call__(self, kook_id: ID, user, **kwargs) -> Result:
        return authorize_admin_only(user, self._command_name())\
                .map(lambda r: self._kook_repository.by_id_with_result(kook_id))\
                .map(lambda r: self.execute_on(r.kook, user, **kwargs))\
                .do(lambda r: self._kook_repository.save(r.kook))

    def execute_on(self, kook: Kook, user: Kook, params: Dict) -> Result:
        pass

    def _command_name(self) -> str:
        return ''.join(' ' + c.lower() if c.isupper() else c for c in self.__class__.__name__).strip()


class ToggleRole(UpdateKookBaseCommand):
    def execute_on(self, kook: Kook, user: Kook, params: Dict={}) -> Result:
        return cannot_change_yourself(kook.id, user, 'change your role') \
            .map(lambda r: Success(kook=kook.toggle_role()))

