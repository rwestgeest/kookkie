from datetime import datetime
from functools import reduce
from typing import Optional, Iterable, List

from quiltz.domain import Success, Failure
from quiltz.domain.results import Result

from app import db
from app.domain import (
    ID,
    KookkieSession,
    KookkieSessionsRepository,
    Kook, KookkieSessionListItem, KookkieSessionEvent, KookkieSessionCreated,
    KookSessionCounts, KookSessionCount, KookkieParticipant,
    KookkieSessionWasDeleted)
from .kookkie_session_record import (
    KookkieSession as KookkieSessionRecord,
    KookkieParticipant as KookkieParticipantRecord)

hard_coded_sessions = [
    KookkieSession(id=ID.from_string('ae5d4c45-3b46-4ad5-b55a-ba25696b9e85'), date="2020-01-11",
                   kook_id=ID.from_string('f894571d-5707-4ea1-86f5-1d421ed37b91'),
                   kook_name='Rob Westgeest', name='Kikkererwten met koes koes'),
    KookkieSession(id=ID.from_string('590a41e9-ae9c-4ba5-b48f-ceef9d62fa70'), date="2020-03-20",
                   kook_id=ID.from_string('a8487ed5-39b4-48da-bf9a-a536e937a85a'),
                   kook_name='Anton Brunt', name='Meat party')
]

KOOKKIE_SESSION_NOT_FOUND = Failure(message='kookkie not found')


class InMemoryKookkieSessionsRepository(KookkieSessionsRepository):
    @classmethod
    def with_hard_coded_values(cls):
        return InMemoryKookkieSessionsRepository(hard_coded_sessions)

    def __init__(self, kookkie_sessions=list()):
        self.kookkie_sessions = { c.id : c for c in kookkie_sessions }

    def all(self, kook: Kook) -> list[KookkieSessionListItem]:
        return sorted([s.as_list_item() for s in self.all_kookkie_sessions() if s.is_accessible_for(kook)],
                      key=lambda s: s.date)

    def count_sessions_by_kooks(self, since: Optional[datetime] = None) -> KookSessionCounts:
        return reduce(lambda counts, session: counts.add(session), self.all_kookkie_sessions(), KookSessionCounts())

    def all_kookkie_sessions(self) -> Iterable[KookkieSession]:
        return self.kookkie_sessions.values()

    def _by_id(self, kookkie_session_id: ID, kook: Optional[Kook]) -> Optional[KookkieSession]:
        try:
            kookkie_session = self.kookkie_sessions[kookkie_session_id]
            if not kook: return kookkie_session
            return kookkie_session.is_accessible_for(kook) and kookkie_session or None
        except KeyError:
            return None

    def by_id_with_result(self, kookkie_session_id: ID, kook: Optional[Kook]) -> Result:
        session = self._by_id(kookkie_session_id, kook)
        return session and Success(kookkie_session=session) or KOOKKIE_SESSION_NOT_FOUND

    def save(self, event: KookkieSessionEvent):
        if isinstance(event, KookkieSessionWasDeleted):
            self.kookkie_sessions.pop(event.kookkie_session.id)
        else:
            self.kookkie_sessions[event.kookkie_session.id] = event.kookkie_session

    def save_all(self, events: list[KookkieSessionEvent]):
        for event in events:
            self.save(event)


class DBKookkieSessionsRepository(KookkieSessionsRepository):
    def all(self, kook: Kook) -> List[KookkieSessionListItem]:
        kook_id = str(kook.id)
        return sorted([as_kookkie_session_list_item(record) for record in KookkieSessionRecord.query.filter(
            KookkieSessionRecord.kook_id == kook_id)],
                      key=lambda s: s.date)

    def _by_id(self, kookkie_session_id: ID, kook: Optional[Kook] = None) -> Optional[KookkieSession]:
        record = self._record_by_id(kookkie_session_id)
        if record is None: return None
        kookkie_session = as_kookkie_session(record)
        if kook and not kookkie_session.is_accessible_for(kook): return None
        return kookkie_session

    def by_id_with_result(self, kookkie_session_id: ID, kook: Optional[Kook]) -> Result:
        session = self._by_id(kookkie_session_id, kook)
        return session and Success(kookkie_session=session) or KOOKKIE_SESSION_NOT_FOUND

    def count_sessions_by_kooks(self, since: Optional[datetime] = None) -> KookSessionCounts:
        query_params = []
        if since is not None:
            query_params.append(KookkieSessionRecord.created_at >= since)

        return KookSessionCounts(
            *[KookSessionCount(
                id=ID.from_string(s.kook_id),
                name=s.kook_name,
                count=c) for (s, c) in db.session.query(KookkieSessionRecord, db.func
                    .count(KookkieSessionRecord.id))
                    .filter(*query_params)
                    .group_by(KookkieSessionRecord.kook_id).all()])

    def _record_by_id(self, kookkie_session_id: ID) -> Optional[KookkieSessionRecord]:
        return KookkieSessionRecord.query.filter_by(id=str(kookkie_session_id)).first()

    def _record_by_id_or_fail(self, kookkie_session_id: ID) -> KookkieSessionRecord:
        record = self._record_by_id(kookkie_session_id)
        if not record:
            raise Exception('Diagnostic session with id {}'.format(str(kookkie_session_id)))
        return record

    def save_all(self, events: list[KookkieSessionEvent]):
        for event in events:
            if isinstance(event, KookkieSessionCreated):
                self._save_created_event(event)
        db.session.commit()

    def save(self, event: KookkieSessionEvent):
        self.save_all([event])

    def _save_created_event(self, event: KookkieSessionCreated):
        kookkie_session = event.kookkie_session
        record = KookkieSessionRecord(
            id=str(kookkie_session.id),
            created_at=event.timestamp,
            date=kookkie_session.date,
            open=kookkie_session.is_open,
            kook_id=str(kookkie_session.kook_id),
            kook_name=kookkie_session.kook_name,
            name=kookkie_session.name)
        db.session.add(record)


    def _to_participant_record(self, participant: KookkieParticipant) -> KookkieParticipantRecord:
        return KookkieParticipantRecord(
            id=str(participant.id),
            joining_id=str(participant.joining_id),
            email=participant.email)


def as_kookkie_session_list_item(record: KookkieSessionRecord) -> KookkieSessionListItem:
    return KookkieSessionListItem(
        id=ID.from_string(record.id),
        date=record.date,
        kook_name=record.kook_name,
        name=record.name)


def as_kookkie_session(record: KookkieSessionRecord) -> KookkieSession:
    return KookkieSession(
        id=ID.from_string(record.id),
        date=record.date,
        kook_id=ID.from_string(record.kook_id),
        kook_name=record.kook_name,
        open=record.open)  # type: ignore


def as_participant(record: KookkieParticipantRecord) -> KookkieParticipant:
    return KookkieParticipant(
        id=ID.from_string(record.id),
        joining_id=ID.from_string(record.joining_id),
        email=record.email and record.email or '')



def potential_none_id(id_str: str) -> Optional[ID]:
    id = ID.from_string(id_str)
    return id if id.valid else None

