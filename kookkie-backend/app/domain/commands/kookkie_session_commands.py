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


class OpenSession:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository):
        self.kookkie_session_repository = kookkie_session_repository

    def __call__(self, session_id: ID, kook: Kook) -> Result:
        return self.kookkie_session_repository.by_id_with_result(session_id, kook) \
            .do(lambda result: self.kookkie_session_repository
                .save(event=KookkieSessionWasOpened(result.kookkie_session.open()))) \
            .map(lambda result: Success())


class CloseSession:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository):
        self.repository = kookkie_session_repository

    def __call__(self, session_id: ID, kook: Kook):
        return self.repository.by_id_with_result(session_id, kook) \
            .map(lambda result: result.kookkie_session.closed().reset_participant_email_addresses()) \
            .do(lambda result:
                [self.repository.save(event=KookkieSessionWasClosed(result.event.kookkie_session)),
                 self.repository.save(event=result.event)])


class JoinSession:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository):
        self.kookkie_session_repository = kookkie_session_repository

    def __call__(self, kookkie_session_id: ID):
        return self.kookkie_session_repository.by_id_with_result(kookkie_session_id, kook=None)


class AddParticipant:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository, id_generator=IDGenerator()):
        self.kookkie_session_repository = kookkie_session_repository
        self.id_generator = id_generator

    def __call__(self, kookkie_session_id: ID, kook: Kook):
        return (self.kookkie_session_repository.by_id_with_result(kookkie_session_id, kook)
                .map(lambda result: result.kookkie_session.add_participant(self.id_generator))
                .do(lambda result: self.kookkie_session_repository.save(result.event))
                .map(lambda result: Success()))


class SetParticipantEmailAddresses:
    def __init__(self, kookkie_session_repository: KookkieSessionsRepository):
        self.kookkie_session_repository = kookkie_session_repository

    def __call__(self, kookkie_session_id: ID, email_addresses_data):
        return self.kookkie_session_repository.by_id_with_result(kookkie_session_id, kook=None) \
            .map(lambda result: result.kookkie_session.set_participant_email_addresses(
                EmailAddresses.from_data(email_addresses_data))) \
            .do(lambda result: self.kookkie_session_repository.save(result.event)) \
            .map(lambda result: Success())
