from app.domain import *
from quiltz.domain.id.testbuilders import aValidID
from datetime import date, timedelta


def aValidKookkieSessionListItem(**kwargs) -> KookkieSessionListItem:
    valid_args = dict(id=aValidID('1'), team='The Team', date='2021-01-30', kook_id=aValidID('100'),
                      is_open=False, is_test=False, is_shared=False, is_archived=False)
    return KookkieSessionListItem(**{**valid_args, **kwargs})


def aValidKookkieSession(**kwargs) -> KookkieSession:
    valid_args = dict(id=aValidID('1'), name='lekker koken', date='2021-01-30', kook_id=aValidID('100'),
                      kook_name='F. Kook')
    return KookkieSession(**{**valid_args, **kwargs})

def aValidJoinInfo(**kwargs) -> JoinInfo:
    valid_args = dict(kookkie=aValidKookkieSession(), jwt=b'some_jwt', room_name="someroom")
    return JoinInfo(**{**valid_args, **kwargs})  # type: ignore

def anOpenKookkieSession(**kwargs) -> KookkieSession:
    extra_args = dict(open=True)
    return aValidKookkieSession(**{**extra_args, **kwargs})


def aValidKookkieSessionCreatedEvent(**kwargs) -> KookkieSessionCreated:
    valid_args = dict(timestamp=Clock.fixed().now(), kookkie_session=aValidKookkieSession())
    return KookkieSessionCreated(**{**valid_args, **kwargs})  # type: ignore


def aValidKookkieParticipant(**kwargs) -> KookkieParticipant:
    valid_args = dict(id=aValidID('33'), joining_id=aValidID('22'),
                      email='participant@email.com')
    return KookkieParticipant(**{**valid_args, **kwargs})


def aValidKook(hashed_password=PasswordHasher().hash('password'), **kwargs) -> Kook:
    valid_args = dict(id=aValidID('100'), email='henk@kooks.com', name='F. Kook',
                      hashed_password=hashed_password,
                      is_admin=False)
    return Kook(**{**valid_args, **kwargs})


def aValidAdministrator(hashed_password=PasswordHasher().hash('password'), **kwargs) -> Kook:
    valid_args = dict(id=aValidID('102'), email='admin@kooks.com', name='P. Kook',
                      hashed_password=hashed_password,
                      is_admin=True)
    return Kook(**{**valid_args, **kwargs})


def aValidPasswordResetToken(token=aValidID('56'), created_time=Clock().now()) -> PasswordResetToken:
    return PasswordResetToken.create_password_reset_token(token=token, created_time=created_time)


def aValidInitialPasswordToken(token=aValidID('56'), created_time=Clock().now()) -> PasswordResetToken:
    return PasswordResetToken.create_initial_password_token(token=token, created_time=created_time)


def anExpiredPasswordResetToken(token=aValidID('56')) -> PasswordResetToken:
    token = aValidPasswordResetToken(token=token)
    token.created_time = token.created_time - timedelta(minutes=PasswordResetToken.PASSWORD_RESET_EXPIRY_IN_MINUTES)
    return token


def aValidKookMessage(**kwargs) -> Message:
    valid_args = dict(to=aValidKook(), subject="Hi There", sender="af@dop.eu", body='Hello Kook')
    return Message.for_named_recipient(**{**valid_args, **kwargs})


def validKookkieSessionCreationParameters(**kwargs):
    return {**dict(date='the date', name='the meal', kook=aValidKook()), **kwargs}


def validKookCreationParameters(**kwargs):
    return {**dict(name='F. Kook', email='frank@hello.com',
                   isAdmin=False), **kwargs}


def validKookUpdateProfileParameters(**kwargs):
    return {**dict(name='F. Kook', email='kook@mail.com',
                   licenseValidUntil=(date.today() + timedelta(weeks=104)).isoformat()), **kwargs}
