from datetime import datetime, timedelta
from dataclasses import dataclass
from quiltz.domain.id import ID


@dataclass
class PasswordResetToken:
    PASSWORD_RESET_EXPIRY_IN_MINUTES=60
    INITIAL_PASSWORD_EXPIRY_IN_MINUTES=60*24

    expiry_in_minutes: int
    token: ID
    created_time: datetime

    @staticmethod
    def create_password_reset_token(token, created_time):
        return PasswordResetToken(expiry_in_minutes=PasswordResetToken.PASSWORD_RESET_EXPIRY_IN_MINUTES, token=token, created_time=created_time)

    @staticmethod
    def create_initial_password_token(token, created_time):
        return PasswordResetToken(expiry_in_minutes=PasswordResetToken.INITIAL_PASSWORD_EXPIRY_IN_MINUTES, token=token, created_time=created_time)

    def is_within_expiry_of(self, user_token):
        if user_token is None: return False
        return self.token == user_token.token and self.created_time < user_token.expiry_time()

    def expiry_time(self):
        return self.created_time + timedelta(minutes=self.expiry_in_minutes)
