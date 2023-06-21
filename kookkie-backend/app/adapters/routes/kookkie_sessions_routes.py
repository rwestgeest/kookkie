import datetime

from flask import jsonify, request, make_response
from app.domain import ID, KookkieSession
from app.domain.commands import *
from .route_builder import RouteBuilder, add_csrf
from .http_response_builders import build_response, from_result_of, not_found, ok, created, bad_request


class KookkieSessionRoutes(object):
    @staticmethod
    def with_kookkie_sessions_repository(kookkie_session_repository, current_user_repository):
        return KookkieSessionRoutes(kookkie_session_repository=kookkie_session_repository,
                                    current_user_repository=current_user_repository,
                                    create_kookkie_session=CreateKookkieSession(kookkie_session_repository))

    def __init__(self, kookkie_session_repository, current_user_repository, create_kookkie_session):
        self.kookkieSessionsRepository = kookkie_session_repository
        self.current_user_repository = current_user_repository
        self.create_kookkie_session = create_kookkie_session

    def register(self, application):
        route = RouteBuilder(application)

        @route('/api/kookkie-sessions', methods=['POST'], login_required=True)
        def create():
            return build_response(from_result_of(self.create_kookkie_session(
                {**request.get_json(), **dict(kook=self.current_user_repository.current_user())}))
                                  .on_success(lambda result: (dict(id=str(result.id)), 201))
                                  .with_csrf())
        return route


        @route('/api/kookkie-sessions', methods=['GET'], login_required=True)
        def all_kookkie_sessions():
            return build_response(from_result_of(Success(kookkies=[]))
                    .on_success(lambda result: ([dict(
                id = IDGenerator().generate_id(),
                date = str(datetime.date.today()),
                name = "Lekker eten met anton",
                kook_name="anton",

            )], 200)).with_csrf())
        return route


