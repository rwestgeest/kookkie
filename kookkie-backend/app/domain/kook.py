from dataclasses import dataclass, replace, field
from typing import Dict

from quiltz.domain import ID, IDGenerator, Success, validate, presence_of, max_length_of, email_validity_of, anonymize
from quiltz.domain.results import Result, Failure


@dataclass
class Kook:
    id: ID
    email: str
    name: str
    hashed_password: str = None
    password_reset_token: str = None
    is_admin: bool = False

    @property
    def username(self):
        return self.email

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)

    @property
    def is_active(self) -> bool:
        return True

    def toggle_role(self):
        return replace(self, is_admin = not self.is_admin)

    def welcome(self, messenger, token_generator) -> "Kook":
        self.password_reset_token = token_generator.generate_initial_token()
        messenger.send_welcome(self)
        return self

    def authenticate(self, unhashed_password, hasher) -> Result:
        if not self._verify(unhashed_password, hasher):
            return Failure(message='Password mismatch for \'{}\''.format(anonymize(self.username)))
        return Success(kook=self)

    def request_password_reset(self, messenger, token_generator) -> "Kook":
        reset_kook = replace(self, password_reset_token=token_generator.generate_token())
        messenger.send_password_reset(reset_kook)
        return reset_kook

    def with_new_password(self, new_password, hasher) -> "Kook":
        return replace(self, hashed_password=hasher.hash(new_password), password_reset_token=None)

    def _verify(self, unhashed_password, hasher) -> bool:
        if not self.hashed_password: return False
        return hasher.verify(unhashed_password=unhashed_password, hashed_password=self.hashed_password)



class KookCreator:
    def __init__(self, id_generator: IDGenerator = IDGenerator()):
        self.id_generator=id_generator

    def create_with_id(self, name:str =None, email:str=None, isAdmin=False):
        return validate(
            presence_of('email', email),
            presence_of('name', name),
            max_length_of('email', email, 320),
            email_validity_of('email', email),
            max_length_of('name', name, 80)
        ).map(lambda valid_parameters:
              Success(kook=Kook(id=self.id_generator.generate_id(), name=name, email=email.strip(), is_admin=isAdmin))
              )

@dataclass
class NullKook:
    name = ''
    email = ''
    is_admin = False

    def get_id(self):
        return None

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False



@dataclass(frozen=True)
class KookSessionCount:
    id: ID
    name: str
    count: int

    def inc(self) -> "KookSessionCount":
        return replace(self, count=self.count + 1)


@dataclass(init=False)
class KookSessionCounts:
    _counts: Dict[ID, KookSessionCount] = field(default_factory=dict)

    def __init__(self, *kook_session_counts):
        self._counts = {c.id: c for c in kook_session_counts}

    @property
    def counts(self):
        return list(self._counts.values())

    def add(self, kookkie_session):
        self._counts[kookkie_session.kook_id] = self.count_for(kookkie_session).inc()
        return self

    def count_for(self, kookkie_session):
        return self._counts.get(kookkie_session.kook_id) or \
               KookSessionCount(id=kookkie_session.kook_id, name=kookkie_session.kook_name,
                                count=0)
