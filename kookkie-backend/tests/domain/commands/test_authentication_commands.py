from testing import *
from app.domain.commands import ResetPassword, RequestPasswordReset, Signin, Signout
from app.domain import PasswordHasher, Clock
from app.domain.password_reset_token_generator import PasswordTokenGeneratorGeneratingWithTimeStamp, FixedPasswordTokenGeneratorGenerating
from app.domain.repositories import InMemoryKookRepository
from domain.builders import *
from app.domain import DummyContext
from support.log_collector import log_collector


def aKookRepositoryWith(*kooks):
    return InMemoryKookRepository(kooks)


def anAuthenticatorAuthenticating(current_user_repository, *kooks):
    return Signin(aKookRepositoryWith(*kooks), current_user_repository=current_user_repository)


class TestAuthenticate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.hasher = PasswordHasher()
        self.current_user_repository = Mock()
        self.kook = aValidKook(email='john@mail.com', hashed_password=self.hasher.hash("Str0ngP@ssw0rd"))
        self.signin = anAuthenticatorAuthenticating(self.current_user_repository, self.kook)
        
    def test_fails_when_user_does_not_exist(self):
        assert_that(self.signin('noone', 'pwd'), equal_to(Failure(message='Unknown user \'noone\'')))

    def test_fails_when_user_signin_fails(self):
        kook = aValidKook(email='john@mail.com', hashed_password=None)
        signin = anAuthenticatorAuthenticating(self.current_user_repository, kook)
        assert_that(signin('john@mail.com', 'pwd'), equal_to(kook.authenticate('pwd', self.hasher)))

    def test_succeeds_when_user_siginin_passes(self):
        assert_that(self.signin('john@mail.com', 'Str0ngP@ssw0rd'), equal_to(Success(kook=self.kook)))
        self.current_user_repository.login.assert_called_with(self.kook)

    def test_logs_info_on_successful_authentication(self, log_collector):
        self.signin('john@mail.com', 'Str0ngP@ssw0rd')
        log_collector.assert_info('Login for \'j***@mail.com\'')

    def test_logs_on_unsuccessful_authentication(self, log_collector):
        self.signin('no@one.com', 'pwd')
        log_collector.assert_warning('Unknown user \'n***@one.com\'')


class TestLogout:
    def test_logout_delegates_to_current_user_repository(self):
        current_user_repository = Mock()
        Signout(current_user_repository)()
        current_user_repository.logout.assert_called()


class TestRequestPasswordReset:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.repo = Mock(InMemoryKookRepository)
        self.password_token_generator = FixedPasswordTokenGeneratorGenerating(aValidID(12))
        self.message_engine = Mock()
        self.messenger_factory = MessengerFactory()
        self.request_password_reset = RequestPasswordReset(
            kook_repository=self.repo, 
            message_engine=self.message_engine, 
            password_reset_token_generator=self.password_token_generator,
            messenger_factory=self.messenger_factory)
        self.context = DummyContext()
        
    def test_saves_a_the_resetted_kookin_the_repo(self):
        kook = aValidKook(email='john@doe.eu')
        self.repo.by_username.return_value = kook
        self.request_password_reset('john@doe.eu', context=self.context)
        reset_kook = kook.request_password_reset(self.messenger_factory.create(self.context), self.password_token_generator)
        self.repo.save.assert_called_once_with(reset_kook)
        self.message_engine.commit.assert_called_once_with(self.messenger_factory.create(self.context).send_password_reset(reset_kook))

    def test_returns_success_if_all_ok(self, log_collector):
        kook = aValidKook(email='john@doe.eu')
        self.repo.by_username.return_value = kook
        result = self.request_password_reset('john@doe.eu', context=self.context)
        assert result == Success()
        log_collector.assert_info('Password reset requested for \'j***@doe.eu\'')

    def test_returns_success_even_if_kook_not_found(self, log_collector):
        self.repo.by_username.return_value = None
        result = self.request_password_reset('john@doe.eu', context=self.context)
        assert result == Success()
        log_collector.assert_warning('Unknown user \'j***@doe.eu\'')

    def test_returns_success_even_if_failed_to_send_mail(self, log_collector):
        kook = aValidKook(email='john@doe.eu')
        self.repo.by_username.return_value = kook
        self.message_engine.commit.return_value = Failure(message='')
        result = self.request_password_reset('john@doe.eu', context=self.context)
        assert result == Success()


class TestResetPassword:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.repo = Mock(InMemoryKookRepository)
        self.call_time = Clock.fixed().now()
        self.reset_password = ResetPassword(kook_repository=self.repo, hasher=self, password_reset_token_generator=PasswordTokenGeneratorGeneratingWithTimeStamp(self.call_time))

    def hash(self, password):
        return password
        
    def test_finds_the_kook_by_password_reset_token(self):
        self.repo.by_token.return_value = aValidKook()
        self.reset_password(new_password='new-password', token=aValidID('111'))
        the_expected_password_reset_token = aValidPasswordResetToken(token=aValidID('111'), created_time=self.call_time)
        self.repo.by_token.assert_called_once_with(the_expected_password_reset_token)

    def test_saves_the_kook_with_updated_password_and_token_removed(self):
        kook = aValidKook(password_reset_token=aValidPasswordResetToken())
        self.repo.by_token.return_value = kook
        self.reset_password(new_password='new-password', token=aValidID('111'))
        expected = kook.with_new_password('new-password', self)
        self.repo.save.assert_called_once_with(expected)

    def test_is_successful_if_all_ok(self, log_collector):
        self.repo.by_token.return_value = aValidKook(email='henk@kooks.com', password_reset_token=aValidPasswordResetToken())
        result = self.reset_password(new_password='new-password', token=aValidID('111'))
        assert result == Success()
        log_collector.assert_info('Password reset for \'h***@kooks.com\'')

    def test_fails_if_token_does_not_exist(self, log_collector):
        self.repo.by_token.return_value = None
        result = self.reset_password(new_password='new-password', token=aValidID('111'))
        assert result == Failure(message='invalid or expired token')
        log_collector.assert_warning('Invalid or expired token \'{}\''.format(aValidID('111')))
