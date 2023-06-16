from testing import *
from app.adapters.routes.flask_login_based_current_user_repository import InMemoryCurrentUserRepository
from app.domain.queries import GetUserProfile
from .routes_tests import RoutesTests, localhost_context
from app.utils.json_converters import json_dumps, json_loads
from app.adapters.routes import UserProfileRoutes, as_user_profile
from app.domain import Success, Failure, NullKook
from domain.builders import aValidKook
from datetime import date


class TestGetUserProfileRoutes(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()

    def create_routes(self):
        self.get_user_profile = GetUserProfile(self.current_user_repository)
        return create_user_profile_routes(get_user_profile=self.get_user_profile).register(self.app)

    def test_returns_null_profile_when_not_logged_in(self):
        response = self.client.get('/api/profile')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json_loads(response.data), equal_to(as_user_profile(NullKook())))

    def test_returns_profile_when_logged_in(self):
        self.do_signin()
        response = self.client.get('/api/profile')
        assert_that(response.status, equal_to('200 OK'))
        assert_that(json_loads(response.data), equal_to(as_user_profile(aValidKook())))

class TestUserProfileMapping:
    def test_contains_name_role_email_license_date(self):
        assert_that(as_user_profile(aValidKook(name='henk', email='henk@mail.com', is_admin=True)),
                    equal_to(dict(name='henk', email='henk@mail.com', role='admin')))

        assert_that(as_user_profile(aValidKook(name='henk', email='henk@mail.com',
                                               is_admin=False)),
                    equal_to(dict(name='henk', email='henk@mail.com',
                                  role='kook')))

    def test_maps_null_kook_to_anonymous_role(self):
        assert_that(as_user_profile(NullKook()), equal_to(dict(name='', email='', role='anonymous')))


def create_user_profile_routes(**kwargs):
    valid_route_params = dict(
        current_user_repository=None,
        get_user_profile=None)
    return UserProfileRoutes(**{ **valid_route_params, **kwargs })
