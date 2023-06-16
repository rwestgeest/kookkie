import pytest
from unittest.mock import Mock
from quiltz.domain.id.testbuilders import aValidID
from domain.builders import aValidKook, aValidPasswordResetToken
from app.domain.queries import CheckPasswordResetToken
from app.domain import Success, Failure, Clock
from app.domain.password_reset_token_generator import PasswordTokenGeneratorGeneratingWithTimeStamp


class TestResetPasswordTokenQuery:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.kook_repo = Mock()
        self.query = CheckPasswordResetToken(self.kook_repo,
          password_reset_token_generator=PasswordTokenGeneratorGeneratingWithTimeStamp(Clock.fixed().now()))

    def test_looks_up_the_token(self):
        self.kook_repo.by_token.return_value = None
        self.query(aValidID('1'))
        self.kook_repo.by_token.assert_called_once_with(
          aValidPasswordResetToken(token=aValidID('1'), 
          created_time=Clock.fixed().now()))

    def test_fails_when_token_expired(self):
        self.kook_repo.by_token.return_value = None
        assert self.query(aValidID('1')) == Failure(message='invalid or expired token')

    def test_succeeds_when_token_is_valid(self):
        self.kook_repo.by_token.return_value = aValidKook()
        assert self.query(aValidID('1')) == Success()
