from app.domain.repositories import CurrentUserRepository


class GetUserProfile:
    def __init__(self, current_user_repository: CurrentUserRepository):
        self.current_user_repository = current_user_repository
        
    def __call__(self):
        return self.current_user_repository.current_user()
