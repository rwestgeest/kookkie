from app.domain.repositories import KookRepository, FACILITATOR_NOT_FOUND, InMemoryKookRepository
from testing import *
from quiltz.domain.id import FixedIDGeneratorGenerating
from app.domain.commands import CreateKook, ToggleRole
from app.domain.password_reset_token_generator import FixedInitialPasswordTokenGeneratorGenerating
from app.adapters.repositories import InMemoryKookkieSessionsRepository
from domain.builders import *
from app.domain import DummyContext
from support.log_collector import log_collector

class TestCreateKookCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = Mock(InMemoryKookRepository)
        self.id_generator = FixedIDGeneratorGenerating(aValidID(12))
        self.password_token_generator = FixedInitialPasswordTokenGeneratorGenerating(aValidID(12))
        self.message_engine = Mock()
        self.messenger_factory = MessengerFactory()
        self.create_kook = CreateKook(
            self.repo, 
            self.message_engine, 
            id_generator=self.id_generator, 
            password_reset_token_generator=self.password_token_generator, 
            messenger_factory=self.messenger_factory)
        self.context = DummyContext()
        self.repo.by_username.return_value = None
        self.message_engine.commit.return_value = Success()

    def test_saves_a_new_welcomed_kook_with_an_id_in_the_repo(self):
        self.create_kook(validKookCreationParameters(), context=self.context, user=aValidAdministrator())
        created_kook = KookCreator(id_generator=self.id_generator).create_with_id(**validKookCreationParameters()).kook.welcome(self.message_engine, token_generator=self.password_token_generator)
        self.repo.save.assert_called_once_with(created_kook)
        self.message_engine.commit.assert_called_once_with(
            self.messenger_factory.create(self.context).send_welcome(created_kook))

    def test_returns_success_if_all_ok(self):
        result = self.create_kook(validKookCreationParameters(), context=self.context,
                                  user=aValidAdministrator())
        assert_that(result, equal_to(Success(id = aValidID('12'))))

    def test_returns_failure_with_actual_failure_message_if_something_failed(self):
        result = self.create_kook(dict(), context=self.context, user=aValidAdministrator())
        assert_that(result, equal_to(Failure(message='email is missing')))
        self.repo.save.assert_not_called()

    def test_fails_if_kook_exists(self):
        self.repo.by_username.return_value = aValidKook(email='existing@mail.com')
        result = self.create_kook(validKookCreationParameters(email='existing@mail.com'),
                                  context=self.context, user=aValidAdministrator())
        self.repo.save.assert_not_called()
        assert_that(result, equal_to(Failure(message='kook already exists')))

    def test_returns_failure_if__the_current_user_is_not_admin(self):
        result = self.create_kook(validKookCreationParameters(), context=self.context,
                                  user=aValidKook())
        assert_that(result, equal_to(Failure(message='not allowed to create a kook')))


class BaseKookUpdateCommandTest(ABC):
    __test__ = False

    @pytest.fixture(autouse=True)
    def setup(self):
        self.kook = aValidKook()
        self.repo = Mock(KookRepository)
        self.repo.by_id_with_result.return_value = Success(kook=self.kook)
        self.command = self.create_command()
        self.command_name = self.command._command_name()

    @abstractmethod
    def create_command(self): pass

    @abstractmethod
    def call_command(self, kook_id: ID, user: Kook): pass

    def test_returns_not_found_when_kook_does_not_exist(self):
        self.repo.by_id_with_result.return_value = Failure(message="Kook does not exist")
        result = self.call_command(kook_id=self.kook.id, user=aValidAdministrator())
        assert_that(result, equal_to(Failure(message="Kook does not exist")))

    def test_does_not_save_on_failure(self):
        self.repo.by_id_with_result.return_value = Failure(message="Kook does not exist")
        self.call_command(kook_id=self.kook.id, user=aValidAdministrator())
        self.repo.save.assert_not_called()

    def test_returns_not_allowed_when_user_is_not_admin(self):
        result = self.call_command(kook_id=self.kook.id, user=aValidKook())
        assert_that(result, equal_to(Failure(message='not allowed to {}'.format(self.command_name))))


class TestToggleRoleCommand(BaseKookUpdateCommandTest):
    __test__ = True

    def create_command(self):
        self.toggle_role = ToggleRole(self.repo)
        return self.toggle_role

    def call_command(self, kook_id, user):
        return self.toggle_role(kook_id=kook_id, user=user)

    def test_changes_role_of_kook(self):
        admin = aValidAdministrator(id=aValidID('400'))
        self.repo.by_id_with_result.return_value = Success(kook=admin)
        result = self.toggle_role(admin.id, aValidAdministrator(id=aValidID('300')))
        assert_that(result, equal_to(Success(kook=admin.toggle_role())))
        self.repo.save.assert_called_once_with(admin.toggle_role())

    def test_cannot_change_your_own_role(self):
        admin = aValidAdministrator(id=aValidID('400'))
        self.repo.by_id_with_result.return_value = Success(kook=admin)
        result = self.toggle_role(admin.id, admin)
        assert_that(result, equal_to(Failure(message='not allowed to change your role yourself')))


