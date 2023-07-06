from quiltz.domain.id import ID, IDGenerator
from quiltz.domain.results import Success, Failure, Result
from quiltz.domain.validator import validate, presence_of, max_length_of, is_between, conversion_of
from .clock import Clock
from .email_addresses import EmailAddress, EmailAddresses
from datetime import date, datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, field
import re

MAX_NUMBER_OF_PARTICIPANTS = 30
UNKNOWN_PARTICIPANT = Failure(message='unknown participant')


@dataclass(init=False)
class KookkieParticipant:
    id: ID
    joining_id: ID
    email: Union[str, None]

    def __init__(self, id, joining_id, answers=None, email=''):
        if answers is None: answers = list()
        self.id = id
        self.joining_id = joining_id
        self.email = email

    @staticmethod
    def generate(id_generator):
        return KookkieParticipant(id=id_generator.generate_id(), joining_id=id_generator.generate_id())


class KookkieSessionCreator:
    def __init__(self, id_generator=IDGenerator(), clock=Clock()):
        self.id_generator=id_generator
        self.clock = clock

    def create_with_id(self, date=None, participant_count=0, kook=None, language="en"):
        return validate(
            presence_of('date', date),
            presence_of('kook', kook),
            is_between('participant_count', participant_count, 1, MAX_NUMBER_OF_PARTICIPANTS),
        ).map(lambda valid_parameters:
            Success(kookkie_session_created=KookkieSessionCreated(timestamp=self.clock.now(),
                                                                     kookkie_session=KookkieSession(
                id = self.id_generator.generate_id(),
                date = valid_parameters.date,
                kook_id=valid_parameters.kook.id,
                kook_name=valid_parameters.kook.name,
                participants=[
                    KookkieParticipant.generate(id_generator=self.id_generator)
                    for x in range(valid_parameters.participant_count)])))
        )


@dataclass(frozen=True)
class KookkieSessionListItem:
    id: ID
    date: date
    kook_name: str
    name: str



@dataclass(init=False)
class KookkieSession(object):
    id: ID
    name: str
    date: date
    kook_id: ID
    kook_name: str
    participants: List[KookkieParticipant]
    _open: bool


    def __init__(self, id: ID,
                 date,
                 kook_id: ID,
                 kook_name: str,
                 participants: List[KookkieParticipant],
                 name: str = "lekker koken",
                 open=False):
        self.id = id
        self.name = name
        self.date = date
        self.kook_id = kook_id
        self.kook_name = kook_name
        self.participants = participants
        self._open = open

    def _participant_by_id(self, participant_id: ID) -> Optional[KookkieParticipant]:
        return next((p for p in self.participants if p.id == participant_id), None)

    def participant_count(self) -> int:
        return len(self.participants)

    def as_list_item(self) -> KookkieSessionListItem:
        return KookkieSessionListItem(
            id=self.id,
            date=self.date,
            kook_name=self.kook_name,
            name=self.name)

    @property
    def is_open(self) -> bool:
        return self._open

    @property
    def room_name(self) -> str:
        return re.sub(r'[ \t]', '', self.name.title())

    def start(self, kook, jwt_builder):
        if (kook.id != self.kook_id):
            return Failure(message="This is not your kookkie")
        return Success(started_kookkie=JoinInfo(kookkie=self, jwt=jwt_builder.for_kook(kook, self.room_name)))

    def open(self) -> 'KookkieSession':
        self._open = True
        return self

    def closed(self) -> 'KookkieSession':
        self._open = False
        return self

    def is_accessible_for(self, kook):
        return self.kook_id == kook.id


@dataclass(frozen=True)
class JoinInfo:
    kookkie: KookkieSession
    jwt: bytes

    @property
    def room_name(self):
        return self.kookkie.room_name


@dataclass(frozen=True)
class KookkieSessionEvent:
    kookkie_session: KookkieSession

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def id(self) -> ID:
        return self.kookkie_session.id


@dataclass(frozen=True)
class KookkieSessionCreated(KookkieSessionEvent):
    timestamp: datetime


@dataclass(frozen=True)
class KookkieSessionWasOpened(KookkieSessionEvent):
    pass


@dataclass(frozen=True)
class KookkieSessionWasClosed(KookkieSessionEvent):
    pass


@dataclass(frozen=True)
class ParticipantWasAdded(KookkieSessionEvent):
    new_participant: KookkieParticipant


@dataclass(frozen=True)
class ParticipantEmailAddressesWereSet(KookkieSessionEvent):
    email_addresses: List[EmailAddress]


@dataclass(frozen=True)
class ParticipantEmailAddressesWereReset(KookkieSessionEvent):
    pass


@dataclass(frozen=True)
class ParticipantsWereInvited(KookkieSessionEvent):
    invited_participants: List[KookkieParticipant]


@dataclass(frozen=True)
class KookkieSessionWasDeleted(KookkieSessionEvent):
    pass


@dataclass(frozen=True)
class KookkieSessionWasArchived(KookkieSessionEvent):
    pass
