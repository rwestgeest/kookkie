from quiltz.domain.id.testbuilders import aValidID

from app.domain.clock import FixedClock
from testing import *
from datetime import date, timedelta
from quiltz.domain.results import Success
from app.adapters.repositories import DBKookRepository, admins
from app.domain.repositories import FACILITATOR_NOT_FOUND
from domain.builders import aValidKook, aValidPasswordResetToken, anExpiredPasswordResetToken, \
    aValidInitialPasswordToken
from app import create_app, db
from app.domain import ID
from app.domain import anonymize
from support.log_collector import log_collector


class BaseDbKookRepositoryTest:
    __test__ = False

    class TestConfig(object):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        TESTING = True
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    @pytest.fixture(autouse=True)
    def setup_db(self):
        the_app = create_app(self.TestConfig)
        with the_app.app_context():
            self.repo = DBKookRepository()
            db.create_all()
            yield


class TestDbKookRepository(BaseDbKookRepositoryTest):
    __test__ = True
    
    def test_an_empty_kook_repo_has_no_items(self):
        assert_that(list(self.repo.all()), equal_to([]))

    def test_creating_a_kook_makes_it_available_in_the_repo(self):
        kook = aValidKook()
        self.repo.save(kook=kook)
        assert_that(list(self.repo.all()), equal_to([kook]))

    def test_creating_a_kook_with_password_reset_token_makes_it_available_in_the_repo(self):
        kook = aValidKook(password_reset_token=aValidPasswordResetToken())
        self.repo.save(kook=kook)
        assert_that(list(self.repo.all()), equal_to([kook]))

    def test_creating_a_kook_with_an_initial_password_token_makes_it_available_in_the_repo(self):
        kook = aValidKook(hashed_password=None, password_reset_token=aValidInitialPasswordToken())
        self.repo.save(kook=kook)
        assert_that(list(self.repo.all()), equal_to([ kook ]))

    def test_saving_a_kook_again_updates_the_repo(self):
        self.repo.save(kook=aValidKook())
        updated_kook = aValidKook(name='Harry', email='harry@mail.com')
        self.repo.save(kook=updated_kook)
        assert_that(list(self.repo.all()), equal_to([ updated_kook ]))

    def test_delete_does_not_affect_other_kooks(self):
        id = ID.from_string('59f989b3-e44d-44ee-8a95-9339354c47eb')
        self.repo.save(aValidKook(id=id))
        repo = self.repo.with_admins().remove(id)
        assert_that(repo.by_id_with_result(admins[0].id).kook, equal_to(admins[0]))
        assert_that(repo.by_id_with_result(admins[1].id).kook, equal_to(admins[1]))

    def test_delete_removes_specific_kook(self):
        id = ID.from_string('59f989b3-e44d-44ee-8a95-9339354c47eb')
        self.repo.save(aValidKook(id=id))
        repo = self.repo.with_admins().remove(id)
        assert_that(repo.by_id_with_result(id).is_failure(), equal_to(True))

    def test_delete_outputs_to_log(self, log_collector):
        id = ID.from_string('59f989b3-e44d-44ee-8a95-9339354c47eb')
        self.repo.save(aValidKook(id=id, email='johnson@email.com'))
        self.repo.with_admins().remove(id)
        log_collector.assert_info("removed kook with id {} and email {}".format(str(id),
                                                                                       anonymize('johnson@email.com')))


class TestDbKookRepositoryWithAdmins(BaseDbKookRepositoryTest):
    __test__ = True

    def test_creates_a_repository_seeded_with_admins(self):
        self.repo.with_admins()
        assert_that(list(self.repo.all()), equal_to(admins))

    def test_creates_admins_only_once(self):
        self.repo.with_admins().with_admins()
        assert_that(list(self.repo.all()), equal_to(admins))


class TestKookRepositoryById(BaseDbKookRepositoryTest):
    __test__ = True
    
    def test_retrieves_a_kook_by_id(self):
        kook = aValidKook(id=aValidID('88'))
        self.repo.save(kook=kook)
        assert_that(self.repo.by_id_with_result(aValidID('88')).kook, equal_to(kook))

    def test_by_id_returns_none_when_kook_cannot_be_found(self):
        assert_that(self.repo.by_id_with_result(aValidID('8888')).is_failure(), equal_to(True))

    def test_retrieves_a_kook_by_id_with_result(self):
        kook = aValidKook(id=aValidID('88'))
        self.repo.save(kook=kook)
        assert_that(self.repo.by_id_with_result(aValidID('88')), equal_to(Success(kook=kook)))

    def test_by_id_with_result_returns_failure_when_kook_cannot_be_found(self):
        assert_that(self.repo.by_id_with_result(aValidID('8888')), equal_to(FACILITATOR_NOT_FOUND))


class TestKookRepositoryByPasswordResetToken(BaseDbKookRepositoryTest):
    __test__ = True
    
    def test_retrieves_a_kook_by_password_reset_token(self):
        password_reset_token = aValidPasswordResetToken()
        kook = aValidKook(password_reset_token=password_reset_token)
        self.repo.save(kook=kook)
        assert_that(self.repo.by_token(password_reset_token), equal_to(kook))

    def test_by_token_returns_none_when_token_cannot_be_found(self):
        assert_that(self.repo.by_token(aValidPasswordResetToken()), equal_to(None))

    def test_by_token_returns_none_when_token_was_expired(self):
        kook = aValidKook(password_reset_token=anExpiredPasswordResetToken())
        self.repo.save(kook=kook)
        assert_that(self.repo.by_token(aValidPasswordResetToken()), equal_to(None))


class TestKookRepositoryByUserName(BaseDbKookRepositoryTest):
    __test__ = True

    def test_retrieves_a_kook_by_username(self):
        kook = aValidKook(email='rob@mail.com')
        self.repo.save(kook=kook)
        assert_that(self.repo.by_username('rob@mail.com'), equal_to(kook))
        assert_that(self.repo.by_username_with_result('rob@mail.com'), equal_to(Success(kook=kook)))

    def test_has_user(self):
        kook = aValidKook(email='rob@mail.com')
        self.repo.save(kook=kook)
        assert_that(self.repo.has_user('rob@mail.com'), equal_to(True))
        assert_that(self.repo.has_user('unknown@mail.com'), equal_to(False))

    def test_by_username_is_case_insensitive_by_storing_lowercase(self):
        kook = aValidKook(email='ROB@mail.com')
        self.repo.save(kook=kook)
        assert_that(self.repo.by_username('rob@mail.com'), equal_to(aValidKook(email='rob@mail.com')))
        assert_that(self.repo.by_username('rob@MaIl.com'), equal_to(aValidKook(email='rob@mail.com')))
        assert_that(self.repo.by_username_with_result('rob@mail.com'), equal_to(Success(kook=aValidKook(email='rob@mail.com'))))
        assert_that(self.repo.by_username_with_result('rob@MaIl.com'), equal_to(Success(kook=aValidKook(email='rob@mail.com'))))

    def test_by_username_returns_none_when_kook_cannot_be_found(self):
        assert_that(self.repo.by_username('xxx'), equal_to(None))
        assert_that(self.repo.by_username_with_result('xxx'), equal_to(FACILITATOR_NOT_FOUND))


class TestKookRepository_defaultKooks(BaseDbKookRepositoryTest):
    __test__ = True
    
    def test_creates_admins_when_they_do_not_exist_yet(self):
        repo = self.repo.with_admins()
        assert_that(repo.by_id_with_result(admins[0].id).kook, equal_to(admins[0]))

    def test_does_not_modify_admins_when_they_already_exist(self):
        repo = self.repo.with_admins()
        admin = repo.by_id_with_result(admins[0].id).kook
        admin.name = 'Henk'
        repo.save(admin)
        repo = repo.with_admins()
        assert_that(repo.by_id_with_result(admins[0].id).kook.name, equal_to('Henk'))

