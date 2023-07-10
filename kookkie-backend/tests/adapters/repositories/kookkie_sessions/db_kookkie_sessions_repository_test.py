from app import create_app, db
from app.adapters.repositories import DBKookkieSessionsRepository
from domain.builders import aValidKookkieSessionCreatedEvent, aValidKook


class DbKookkieSessionsRepositoryTest:
    __test__ = False

    class TestConfig(object):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        TESTING = True
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    def a_db_with(self, *kookkie_sessions):
        the_app = create_app(self.TestConfig)
        with the_app.app_context():
            self.repo = DBKookkieSessionsRepository()
            db.create_all()
            for session in kookkie_sessions:
                self.repo.save(aValidKookkieSessionCreatedEvent(kookkie_session=session))
        return the_app.app_context()


