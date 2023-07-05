from flask import jsonify, request, make_response
from app.domain import ID, KookkieSession, JoinInfo
from app.domain.commands import *
from .route_builder import RouteBuilder, add_csrf
from .http_response_builders import build_response, from_result_of, not_found, ok, created, bad_request


class KookkieSessionRoutes(object):
    @staticmethod
    def with_kookkie_sessions_repository(kookkie_session_repository, current_user_repository, jaas_jwt_builder):
        return KookkieSessionRoutes(kookkie_session_repository=kookkie_session_repository,
                                    current_user_repository=current_user_repository,
                                    create_kookkie_session=CreateKookkieSession(kookkie_session_repository),
                                    start_kookkie_session=StartKookkieSession(kookkie_session_repository, jaas_jwt_builder))

    def __init__(self, kookkie_session_repository,
                 current_user_repository,
                 create_kookkie_session,
                 start_kookkie_session):
        self.kookkieSessionsRepository = kookkie_session_repository
        self.current_user_repository = current_user_repository
        self.create_kookkie_session = create_kookkie_session
        self.start_kookkie_session = start_kookkie_session

    def register(self, application):
        route = RouteBuilder(application)

        @route('/api/kookkie-sessions', methods=['POST'], login_required=True)
        def create():
            return build_response(from_result_of(self.create_kookkie_session(
                {**request.get_json(), **dict(kook=self.current_user_repository.current_user())}))
                                  .on_success(lambda result: (dict(id=str(result.id)), 201))
                                  .with_csrf())


        @route('/api/kookkie-sessions', methods=['GET'], login_required=True)
        def all_kookkie_sessions():
            return build_response(from_result_of(Success(kookkies=[]))
                    .on_success(lambda result: ([dict(
                id = str(IDGenerator().generate_id()),
                date = "2023-06-07",
                name = "Lekker eten met anton",
                kook_name="anton",
            )], 200)).with_csrf())

        @route('/api/kookkie-sessions/<kookkie_id>/start', methods=['POST'], login_required=True)
        def start(kookkie_id):
            return build_response(from_result_of(self.start_kookkie_session(kookkie_id=ID.from_string(kookkie_id),
                                                                            kook=self.current_user_repository.current_user()))
                                  .on_success(lambda result: (as_started_kookkie(result.started_kookkie), 201))
                                  .with_csrf())

        return route



def as_started_kookkie(started_kookkie:JoinInfo):
    return dict(
        jwt=started_kookkie.jwt.decode(),
        room_name=started_kookkie.room_name,
        kookkie=as_kookkie_session(started_kookkie.kookkie)
    )

def as_kookkie_session(kookkie_session):
    return dict(id=str(kookkie_session.id),
                name=kookkie_session.name,
                date=kookkie_session.date,
                kook_name=kookkie_session.kook_name)