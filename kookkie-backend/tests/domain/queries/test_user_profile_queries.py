from app.domain.repositories.current_user_repository import StubbedCurrentUserRepository
from domain.builders import aValidKook
from app.domain.queries import GetUserProfile


class TestGetUserProfileQuery:
    def test_returns_the_current_user_profile(self):
        current_user_repo = StubbedCurrentUserRepository(aValidKook())
        query = GetUserProfile(current_user_repo)
        assert query() == aValidKook()
