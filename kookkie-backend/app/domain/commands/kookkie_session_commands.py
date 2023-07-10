import logging
from typing import Optional
from quiltz.domain import ID
from quiltz.domain.id import IDGenerator
from quiltz.domain.results import Result

from app.domain import (
    KookkieSessionCreator,
    Clock,
    Success,
    Failure,
    KookkieSessionWasOpened,
    KookkieSessionWasClosed,
    Kook, KookkieSessionsRepository)
from app.domain.email_addresses import EmailAddresses
from app.domain.repositories import KookRepository
from app.utils.jaas_jwt_builder import JaaSJwtBuilder


class CreateKookkieSession:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository, id_generator=IDGenerator(),
                 clock=Clock()):
        self.id_generator = id_generator
        self.repo = kookkie_session_repository
        self.clock = clock

    def __call__(self, attributes):
        result = KookkieSessionCreator(id_generator=self.id_generator,
                                       clock=self.clock).create_with_id(**attributes)
        if not result.is_success():
            return Failure(message='failed to create kookkie session')

        self.repo.save(event=result.kookkie_session_created)
        return Success(id=result.kookkie_session_created.id)


class StartKookkieSession:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository, jaas_jwt_builder: JaaSJwtBuilder):
        self.jaas_jwt_builder = jaas_jwt_builder
        self.kookkie_session_repository = kookkie_session_repository

    def __call__(self, kookkie_id, kook):
        return self.kookkie_session_repository.by_id_with_result(kookkie_id)\
            .map(lambda result: result.kookkie_session.start(kook, self.jaas_jwt_builder))


class JoinSession:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository, jaas_jwt_builder: JaaSJwtBuilder):
        self.jaas_jwt_builder = jaas_jwt_builder
        self.kookkie_session_repository = kookkie_session_repository

    def __call__(self, kookkie_session_id: ID, name=""):
        return self.kookkie_session_repository.by_id_with_result(kookkie_session_id, kook=None) \
            .map(lambda result: result.kookkie_session.join(name, self.jaas_jwt_builder))

