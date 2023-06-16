from . import ok, bad_request
from .http_response_builders import no_content
from .route_builder import RouteBuilder
from app.domain.queries import GetUserProfile
from flask import request

from ...domain import Kook, Clock
from ...domain.repositories import CurrentUserRepository


class UserProfileRoutes:
    @staticmethod
    def create(current_user_repository: CurrentUserRepository):
        return UserProfileRoutes(current_user_repository,
                                 get_user_profile=GetUserProfile(current_user_repository))

    def __init__(self, current_user_repository: CurrentUserRepository, get_user_profile: GetUserProfile):
        self.current_user_repository = current_user_repository
        self.get_user_profile = get_user_profile

    def register(self, app):
        route = RouteBuilder(app)

        @route('/api/profile', methods=['GET'], login_required=False)
        def get_user_profile():
            return as_user_profile(self.get_user_profile())

        return route

def as_user_profile(kook: Kook):
    result: dict[str, object] = \
        dict(name=kook.name, email=kook.email,
             role='admin' if kook.is_admin else 'anonymous' if kook.is_anonymous else 'kook')
    return result
