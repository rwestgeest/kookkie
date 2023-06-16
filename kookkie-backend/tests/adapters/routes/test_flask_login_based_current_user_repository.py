from quiltz.domain.id.testbuilders import aValidID
from testing import *
from app.adapters.routes import FlaskLoginBasedCurrentUserRepository, InMemoryCurrentUserRepository
from app.domain.repositories import InMemoryKookRepository
from domain.builders import aValidKook


class TestInMemoryCurrentUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = aValidKook()
        self.user_repo = InMemoryCurrentUserRepository()

    def test_returns_logged_in_user(self):
        self.user_repo.login(self.user)
        assert_that(self.user_repo.current_user(), equal_to(self.user))

    def test_has_no_current_user_after_logout(self):
        self.user_repo.login(self.user)
        self.user_repo.logout()
        assert_that(self.user_repo.current_user(), equal_to(None))


class TestFlaskLoginBasedCurrentUserRepository_load_user:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.kook = aValidKook(id=aValidID('33'))
        user_repo = InMemoryKookRepository([self.kook])
        self.authenticator = FlaskLoginBasedCurrentUserRepository(user_repo)

    def test_returns_user_by_id(self):
        assert self.authenticator._load_user(str(aValidID('33'))) == self.kook

    def test_can_handle_UUID_objects_for_backwards_compatibility(self):
        assert self.authenticator._load_user(aValidID('33')._uuid) == self.kook
