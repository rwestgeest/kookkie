from app.domain import Success, Failure, PasswordHasher, anonymize
from app.domain.password_reset_token_generator import PasswordResetTokenGenerator
import logging


class Signin:
    def __init__(self, user_repository, current_user_repository, password_hasher=PasswordHasher()):
        self.user_repository = user_repository
        self.current_user_repository = current_user_repository
        self.password_hasher = password_hasher
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def __call__(self, username, password):
        return self.log_result_of(self._find_user(username)
            .map(lambda r: r.kook.authenticate(password, self.password_hasher))
            .do(lambda r: self.current_user_repository.login(r.kook)))

    def log_result_of(self, result):
        if result.is_success():
            self.logger.info('Login for \'%s\'', anonymize(result.kook.email))
        else:
            self.logger.warning(result.message)
        return result

    def _find_user(self, username):
        user = self.user_repository.by_username(username)
        if not user:
            result = Failure(message='Unknown user \'{}\''.format(anonymize(username)))
        else:
            result = Success(kook=user)
        return result


class Signout:
    def __init__(self, current_user_repository):
        self.current_user_repository = current_user_repository

    def __call__(self):
        self.current_user_repository.logout()


class RequestPasswordReset:
    def __init__(self, kook_repository, message_engine, messenger_factory, password_reset_token_generator=PasswordResetTokenGenerator()):
        self.kook_repository = kook_repository
        self.password_reset_token_generator = password_reset_token_generator
        self.message_engine=message_engine
        self.messenger_factory=messenger_factory
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, username, context):
        kook = self.kook_repository.by_username(username)
        if not kook:
            self.logger.warning('Unknown user \'%s\'', anonymize(username))
            return Success()

        messenger=self.messenger_factory.create(context)
        self.kook_repository.save(kook.request_password_reset(messenger, self.password_reset_token_generator))
        self.message_engine.commit(messenger)
        self.logger.info('Password reset requested for \'%s\'', anonymize(username))
        return Success()


class ResetPassword:
    def __init__(self, kook_repository, hasher=PasswordHasher(), password_reset_token_generator=PasswordResetTokenGenerator()):
        self.kook_repository = kook_repository
        self.hasher = hasher
        self.password_reset_token_generator = password_reset_token_generator
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def __call__(self, new_password, token):
        kook = self.kook_repository.by_token(self.password_reset_token_generator.from_id(token))
        if not kook:
            self.logger.warning('Invalid or expired token \'%s\'', token)
            return Failure(message='invalid or expired token')
        updated = kook.with_new_password(new_password, hasher=self.hasher)
        self.kook_repository.save(updated)
        self.logger.info('Password reset for \'%s\'', anonymize(kook.username))
        return Success()
