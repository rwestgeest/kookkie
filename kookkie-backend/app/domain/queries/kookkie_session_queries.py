from app.domain import Success


class GetKookkieSessionQuery:
    def __init__(self, kookkie_session_repository, kook_repository):
        self.kookkie_session_repository = kookkie_session_repository
        self.kook_repository = kook_repository

    def __call__(self, kookkie_session_id, kook):
        return self.kookkie_session_repository.by_id_with_result(kookkie_session_id, kook)

