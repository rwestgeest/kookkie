from quiltz.domain.id.testbuilders import aValidID
from quiltz.domain.results import Success

from app.domain import ID
from app.domain import PasswordHasher
from app.domain.repositories import FACILITATOR_NOT_FOUND, InMemoryKookRepository
from domain.builders import aValidKook, aValidPasswordResetToken, anExpiredPasswordResetToken
from testing import *


class TestInMemoryUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        hasher = PasswordHasher()
        self.henk = aValidKook(id=aValidID('1'), email='henk@mail.com', hashed_password=hasher.hash('pwd'))
        self.piet = aValidKook(id=aValidID('2'), email='piet@mail.com', hashed_password=hasher.hash('pwd2'))
        self.repository = InMemoryKookRepository([self.henk, self.piet])

    def test_finds_user_by_id(self):
        assert_that(self.repository.by_id_with_result(aValidID('1')), equal_to(Success(kook=self.henk)))
        assert_that(self.repository.by_id_with_result(aValidID('2')), equal_to(Success(kook=self.piet)))

    def test_finds_none_when_no_user_with_that_id(self):
        assert_that(self.repository.by_id_with_result(aValidID('999')), equal_to(FACILITATOR_NOT_FOUND))

    def test_has_user(self):
        assert_that(self.repository.has_user('henk@mail.com'), equal_to(True))
        assert_that(self.repository.has_user('unknown@mail.com'), equal_to(False))

    def test_finds_user_by_username(self):
        assert_that(self.repository.by_username('henk@mail.com'), equal_to(self.henk))
        assert_that(self.repository.by_username('piet@mail.com'), equal_to(self.piet))
        assert_that(self.repository.by_username_with_result('henk@mail.com'), equal_to(Success(kook=self.henk)))
        assert_that(self.repository.by_username_with_result('piet@mail.com'), equal_to(Success(kook=self.piet)))

    def test_by_username_is_case_insensitive(self):
        kook = aValidKook(email='ROB@mail.com')
        self.repository.save(kook=kook)
        assert_that(self.repository.by_username('rob@mail.com'), equal_to(kook))
        assert_that(self.repository.by_username('rob@MaIl.com'), equal_to(kook))
        assert_that(self.repository.by_username_with_result('rob@mail.com'), equal_to(Success(kook=kook)))
        assert_that(self.repository.by_username_with_result('rob@MaIl.com'), equal_to(Success(kook=kook)))

    def test_finds_none_when_no_user_with_that_username(self):
        assert_that(self.repository.by_username('xxxx'), equal_to(None))
        assert_that(self.repository.by_username_with_result('xxxx'), equal_to(FACILITATOR_NOT_FOUND))

    def test_delete_does_not_affect_other_kooks(self):
        id = ID.from_string('59f989b3-e44d-44ee-8a95-9339354c47eb')
        self.repository.save(aValidKook(id=id))
        self.repository.remove(id)
        assert_that(self.repository.by_id_with_result(self.henk.id), equal_to(Success(kook=self.henk)))
        assert_that(self.repository.by_id_with_result(self.piet.id), equal_to(Success(kook=self.piet)))

    def test_delete_removes_specific_kook(self):
        id = ID.from_string('59f989b3-e44d-44ee-8a95-9339354c47eb')
        self.repository.save(aValidKook(id=id))
        self.repository.remove(id)
        assert_that(self.repository.by_id_with_result(id).is_failure(), equal_to(True))


class TestInMemoryUserRepositorySave:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = InMemoryKookRepository.empty()

    def test_appends_new_kook_to_repo(self):
        henk = aValidKook()
        self.repository.save(henk)
        assert_that(self.repository.by_id_with_result(henk.id).kook, equal_to(henk))

    def test_updates_kook_when_it_exists(self):
        self.repository.save(aValidKook(id=aValidID('35')))
        henk = aValidKook(id=aValidID('35'), name='Henk')
        self.repository.save(henk)
        assert_that(self.repository.by_id_with_result(henk.id).kook, equal_to(henk))


class TestInMemoryUserRepositoryByToken:
    def test_finds_nothing_when_theres_no_such_token(self):
        repository = a_repo_with(aValidKook(password_reset_token=aValidPasswordResetToken(token=aValidID('32'))))
        assert_that(repository.by_token(aValidPasswordResetToken(token=aValidID('44'))), equal_to(None))

    def test_finds_kook_by_password_reset_token(self):
        the_token = aValidPasswordResetToken()
        henk = aValidKook(password_reset_token=the_token)
        repository = a_repo_with(henk)
        assert_that(repository.by_token(the_token), equal_to(henk))

    def test_by_token_returns_none_when_token_was_expired(self):
        kook = aValidKook(password_reset_token=anExpiredPasswordResetToken())
        repository = a_repo_with(kook)
        assert_that(repository.by_token(aValidPasswordResetToken()), equal_to(None))

    def test_does_not_explode_when_there_are_users_without_a_token(self):
        repository = a_repo_with(aValidKook(password_reset_token=None))
        assert_that(repository.by_token(aValidPasswordResetToken(token=aValidID('44'))), equal_to(None))


def a_repo_with(*users):
    return InMemoryKookRepository(users)

