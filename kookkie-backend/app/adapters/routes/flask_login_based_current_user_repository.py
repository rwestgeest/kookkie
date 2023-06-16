from flask import session
from flask_login import LoginManager, login_user, logout_user, current_user
from app.domain import ID, NullKook
from app.domain.repositories import CurrentUserRepository


class InMemoryCurrentUserRepository(CurrentUserRepository):
    def login(self, user):
        self._current_user = user

    def current_user(self):
        return self._current_user

    def logout(self):
        self._current_user = None


class FlaskLoginBasedCurrentUserRepository(CurrentUserRepository):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register(self, app):
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.session_protection = "strong"
        login_manager.anonymous_user = NullKook
        
        @login_manager.user_loader
        def load_user(userid):
            return self._load_user(userid)
        return self

    def _load_user(self, userid):
        user = self.user_repository.by_id_with_result(ID.from_string(str(userid)))
        return user.is_success() and user.kook or None

    def login(self, user):
        session.permanent = True
        return login_user(user)

    def current_user(self):
        return current_user._get_current_object()

    def logout(self):
        logout_user()
