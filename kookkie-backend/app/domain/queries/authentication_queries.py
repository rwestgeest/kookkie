from app.domain import Success, Failure
from app.domain.password_reset_token_generator import PasswordResetTokenGenerator


class CheckPasswordResetToken:
    def __init__(self, kook_repository, password_reset_token_generator=PasswordResetTokenGenerator()):
        self.kook_repository = kook_repository
        self.password_reset_token_generator = password_reset_token_generator

    def __call__(self, token):
        if self.kook_repository.by_token(self.password_reset_token_generator.from_id(token)):
            return Success()
        return Failure(message='invalid or expired token')
