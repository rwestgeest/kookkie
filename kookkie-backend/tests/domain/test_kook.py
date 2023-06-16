from app.domain.clock import Clock, FixedClock
from app.domain.dummy_context import DummyContext
from app.domain.messenger import Messages
from testing import *
from datetime import date, timedelta
from hamcrest import is_
from quiltz.domain.id import FixedIDGeneratorGenerating
from quiltz.domain.anonymizer import anonymize
from quiltz.domain.results import Failure, Success
from quiltz.domain.id.testbuilders import aValidID
from app.domain import PasswordHasher, MessengerFactory, FrontEndContext, KookCreator
from app.domain.password_reset_token_generator import FixedInitialPasswordTokenGeneratorGenerating, \
    FixedPasswordTokenGeneratorGenerating
from domain.builders import aValidInitialPasswordToken, \
    validKookCreationParameters, aValidKook, aValidPasswordResetToken, aValidAdministrator


class TestKookkie:

    def test_changes_role_from_admin_to_kook(self):
        assert_that(aValidAdministrator().toggle_role().is_admin, is_(False))

    def test_changes_role_from_kook_to_admin(self):
        assert_that(aValidKook().toggle_role().is_admin, is_(True))


class TestCreateWithId:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.id_generator = FixedIDGeneratorGenerating(aValidID('12'))
        self.creator = KookCreator(id_generator=self.id_generator)

    def test_creates_a_kook_with_a_generated_id(self):
        kook = self.creator.create_with_id(**validKookCreationParameters()).kook
        assert_that(kook.id, equal_to(aValidID('12')))

    def test_creates_a_kook_with_admin_rights(self):
        kook = self.creator.create_with_id(**validKookCreationParameters(isAdmin=True)).kook
        assert_that(kook.is_admin, equal_to(True))

    def test_trims_email_address(self):
        kook = self.creator.create_with_id(
            **validKookCreationParameters(email='\u00a0 henk@email.com  \t ')).kook
        assert_that(kook.username, equal_to('henk@email.com'))

    def test_assigns_all_other_attributes(self):
        license_valid_until = date.today() + timedelta(days=1)
        kook = self.creator.create_with_id(email='henk@email.com', name="henk van der graaf").kook
        assert_that(kook.name, equal_to("henk van der graaf"))
        assert_that(kook.username, equal_to("henk@email.com"))
        assert_that(kook.hashed_password, equal_to(None))

    def test_fails_when_username_is_not_present(self):
        assert_that(self.creator.create_with_id(**validKookCreationParameters(email=None)),
                    equal_to(Failure(message='email is missing')))

    def test_fails_when_username_is_too_long(self):
        assert_that(self.creator.create_with_id(**validKookCreationParameters(email='x' * 321)),
                    equal_to(Failure(message='email is too long')))

    def test_fails_when_username_is_not_valid(self):
        assert_that(self.creator.create_with_id(**validKookCreationParameters(email='xxx')),
                    equal_to(Failure(message='email does not contain a valid email address')))

    def test_fails_when_name_is_not_present(self):
        assert_that(self.creator.create_with_id(**validKookCreationParameters(name=None)),
                    equal_to(Failure(message='name is missing')))

    def test_fails_when_name_is_too_long(self):
        assert_that(self.creator.create_with_id(**validKookCreationParameters(name='x' * 81)),
                    equal_to(Failure(message='name is too long')))


class TestSignIn:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.hasher = PasswordHasher()
        self.kook = aValidKook(email='henk@qwan.eu', hashed_password=self.hasher.hash('Str0ngP@ssw0rd'))

    def test_fails_when_kook_does_not_have_a_password_yet(self):
        kook = aValidKook(email='henk@qwan.eu', hashed_password=None)
        assert_that(kook.authenticate('pwd', self.hasher),
                    equal_to(Failure(message='Password mismatch for \'{}\''.format(anonymize('henk@qwan.eu')))))

    def test_fails_when_password_does_not_match(self):
        assert_that(self.kook.authenticate('WrongPassword', self.hasher),
                    equal_to(Failure(message='Password mismatch for \'{}\''.format(anonymize('henk@qwan.eu')))))

    def test_succeeds_when_user_exist_and_password_matches(self):
        assert_that(self.kook.authenticate('Str0ngP@ssw0rd', self.hasher),
                    equal_to(Success(kook=self.kook)))


class TestWelcome:
    def test_sends_welcome_message(self):
        messenger = MessengerFactory().create(context=FrontEndContext('baseurl/'))
        kook = aValidKook()
        the_token = aValidInitialPasswordToken()
        kook.welcome(messenger, token_generator=FixedInitialPasswordTokenGeneratorGenerating(the_token))
        assert_that(messenger, equal_to(messenger.send_welcome(aValidKook(password_reset_token=the_token))))
