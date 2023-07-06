from typing import Optional
from datetime import date, timezone, datetime
from app.domain import ID
from app import db
from app.domain import Kook, PasswordResetToken, anonymize
from app.domain.repositories import KookRepository, FACILITATOR_NOT_FOUND, admins
from quiltz.domain.results import Success, Result
from .kook_record import Kook as KookRecord
import logging


class DBKookRepository(KookRepository):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def with_admins(self) -> 'DBKookRepository':
        for admin in admins:
            if not self._by_id(admin.id): self.save(admin)
        return self

    def repair(self) -> 'DBKookRepository':
        return self

    def remove(self, id: ID) -> 'DBKookRepository':
        to_delete = find_first_kook_record_by(id=str(id))
        if to_delete is not None:
            db.session.delete(to_delete)
            db.session.commit()
            self.logger.info('removed kook with id %s and email %s', str(id), anonymize(to_delete.email))
        return self

    def all(self) -> list[Kook]:
        return list(map(as_kook, KookRecord.query.all()))

    def save(self, kook: Kook):
        record = KookRecord(
            id=str(kook.id),
            email=kook.email.lower(),
            name=kook.name,
            hashed_password=kook.hashed_password,
            is_admin=kook.is_admin,
            password_reset_token=str(kook.password_reset_token.token) if kook.password_reset_token else None,
            password_reset_token_created_time=kook.password_reset_token.created_time if kook.password_reset_token else None)

        if find_first_kook_record_by(id=str(kook.id)):
            db.session.merge(record)
        else:
            db.session.add(record)

        db.session.commit()

    def _by_id(self, kook_id: ID) -> Optional[Kook]:
        result = find_first_kook_record_by(id=str(kook_id))
        return as_kook(result) if result else None

    def by_id_with_result(self, kook_id: ID) -> Result:
        result = self._by_id(kook_id)
        return Success(kook=result) if result else FACILITATOR_NOT_FOUND

    def has_user(self, username) -> bool:
        return self.by_username(username) is not None

    def by_username(self, username: str) -> Optional[Kook]:
        result = find_first_kook_record_by(email=username.lower())
        return as_kook(result) if result else None

    def by_username_with_result(self, username: str):
        result = find_first_kook_record_by(email=username.lower())
        return Success(kook=as_kook(result)) if result else FACILITATOR_NOT_FOUND

    def by_token(self, token: PasswordResetToken) -> Optional[Kook]:
        result = find_first_kook_record_by(password_reset_token=str(token.token))
        if result is None: return None
        kook = as_kook(result)
        return kook if token.is_within_expiry_of(kook.password_reset_token) else None


def find_first_kook_record_by(**query) -> Optional[KookRecord]:
    return KookRecord.query.filter_by(**query).first()


def as_kook(record: KookRecord) -> Kook:
    return Kook(
        id=ID.from_string(record.id), 
        email=record.email, 
        name=record.name, 
        hashed_password=record.hashed_password,
        is_admin=record.is_admin,
        password_reset_token=as_password_reset_token(record.hashed_password,
                                                     record.password_reset_token,
                                                     record.password_reset_token_created_time)
    )


def as_password_reset_token(password: Optional[str], token: Optional[str], created_time: datetime):
    if not token or not created_time: return None
    created_time = created_time.replace(tzinfo=timezone.utc)
    if password:
        return PasswordResetToken.create_password_reset_token(token=ID.from_string(token), created_time=created_time)
    else:
        return PasswordResetToken.create_initial_password_token(token=ID.from_string(token), created_time=created_time)


