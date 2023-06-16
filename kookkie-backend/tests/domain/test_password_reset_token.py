import pytest
from datetime import timedelta
from quiltz.domain.id import FixedIDGeneratorGenerating
from quiltz.domain.id.testbuilders import aValidID
from app.domain import PasswordResetToken, PasswordResetTokenGenerator, Clock
from domain.builders import aValidInitialPasswordToken, aValidPasswordResetToken


class TestPasswordResetTokenGenerator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.generator = PasswordResetTokenGenerator(id_generator=FixedIDGeneratorGenerating(aValidID('23')))
        
    def test_generate_uses_id_generator_to_generate_password_reset_token(self):
        password_reset_token = self.generator.generate_token()
        assert password_reset_token.token == aValidID('23')

    def test_generate_generates_with_a_brand_new_timestamp(self):
        before = Clock().now()
        password_reset_token = self.generator.generate_token()
        after = Clock().now()
        assert password_reset_token.created_time >= before
        assert password_reset_token.created_time <= after

    def test_generate_initial_generates_token_with_long_expiry(self):
        initial_password_token = self.generator.generate_initial_token()
        assert initial_password_token.expiry_in_minutes == PasswordResetToken.INITIAL_PASSWORD_EXPIRY_IN_MINUTES

    def test_from_uuid_generates_a_password_reset_token_with_that_id(self):
        password_reset_token = self.generator.from_id(aValidID('23'))
        assert password_reset_token.token == aValidID('23')

    def test_from_uuid_generates_with_a_brand_new_timestamp(self):
        before = Clock().now()
        password_reset_token = self.generator.from_id(aValidID(''))
        after = Clock().now()
        assert password_reset_token.created_time >= before
        assert password_reset_token.created_time <= after


class TestPasswordResetToken:
    def test_is_not_within_expiry_of_when_token_has_expired(self):
        current_time = Clock().now()
        assert not aValidPasswordResetToken(created_time=current_time+timedelta(minutes=PasswordResetToken.PASSWORD_RESET_EXPIRY_IN_MINUTES)).is_within_expiry_of(aValidPasswordResetToken(created_time=current_time))

    def test_is_within_expiry_of_when_token_has_not_expired(self):
        current_time = Clock().now()
        assert aValidPasswordResetToken(created_time=current_time).is_within_expiry_of(aValidPasswordResetToken(created_time=current_time))

    def test_is_within_expiry_of_when_token_has_almost_expired(self):
        current_time = Clock().now()
        assert aValidPasswordResetToken(created_time=current_time+timedelta(minutes=PasswordResetToken.PASSWORD_RESET_EXPIRY_IN_MINUTES-1)).is_within_expiry_of(aValidPasswordResetToken(created_time=current_time))

    def test_is_not_within_expiry_of_when_token_is_none(self):
        current_time = Clock().now()
        assert not aValidPasswordResetToken(created_time=current_time).is_within_expiry_of(None)


class TestInitialPasswordToken:
    def test_is_not_within_expiry_of_when_token_has_expired(self):
        current_time = Clock().now()
        assert not aValidInitialPasswordToken(created_time=current_time+timedelta(minutes=PasswordResetToken.INITIAL_PASSWORD_EXPIRY_IN_MINUTES)).is_within_expiry_of(aValidPasswordResetToken(created_time=current_time))

    def test_is_within_expiry_of_when_token_has_not_expired(self):
        current_time = Clock().now()
        assert aValidInitialPasswordToken(created_time=current_time).is_within_expiry_of(aValidInitialPasswordToken(created_time=current_time))

    def test_is_within_expiry_of_when_token_has_almost_expired(self):
        current_time = Clock().now()
        assert aValidInitialPasswordToken(created_time=current_time+timedelta(minutes=PasswordResetToken.INITIAL_PASSWORD_EXPIRY_IN_MINUTES-1)).is_within_expiry_of(aValidInitialPasswordToken(created_time=current_time))

    def test_is_not_within_expiry_of_when_token_is_none(self):
        current_time = Clock().now()
        assert not aValidInitialPasswordToken(created_time=current_time).is_within_expiry_of(None)
        