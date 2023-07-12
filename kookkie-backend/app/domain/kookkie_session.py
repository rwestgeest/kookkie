import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Union

from quiltz.domain.id import ID, IDGenerator
from quiltz.domain.results import Success, Failure, Result
from quiltz.domain.validator import validate, presence_of, is_between, Validator

from .clock import Clock

MAX_NUMBER_OF_PARTICIPANTS = 30


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
        self.id_generator = id_generator
        self.clock = clock

    def create_with_id(self, date=None, name=None, kook=None, language="en"):
        return validate(
            presence_of('date', date),
            presence_of('name', name),
            presence_of('kook', kook),
            non_emptyness_of('name', name),
            non_emptyness_of('date', date)
        ).map(lambda valid_parameters:
              Success(kookkie_session_created=KookkieSessionCreated(timestamp=self.clock.now(),
                                                                    kookkie_session=KookkieSession(
                                                                        id=self.id_generator.generate_id(),
                                                                        date=valid_parameters.date,
                                                                        name=valid_parameters.name,
                                                                        kook_id=valid_parameters.kook.id,
                                                                        kook_name=valid_parameters.kook.name)))
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
    _open: bool

    def __init__(self, id: ID,
                 date,
                 kook_id: ID,
                 kook_name: str,
                 name: str,
                 open=False):
        self.id = id
        self.name = name
        self.date = date
        self.kook_id = kook_id
        self.kook_name = kook_name
        self._open = open

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
        return Success(started_kookkie=jwt_builder.join_info_for_kook(kook, self))

    def join(self, guest, jwt_builder) -> Result:
        return Success(started_kookkie=jwt_builder.join_info_for_guest(guest, self))

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
    room_name: str


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
class KookkieSessionWasDeleted(KookkieSessionEvent):
    pass



def non_emptyness_of(parameter, value):
    return NonEmptynessOf(parameter, value)


class NonEmptynessOf(Validator):
    def validate(self, results):
        if self.value.strip() == '':
            return Failure(message="{} is empty".format(self.parameter_name))
        results.add(self.parameter_name, self.value)
        return Success()

