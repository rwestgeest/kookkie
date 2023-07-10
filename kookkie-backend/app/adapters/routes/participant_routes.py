from flask import jsonify, request
from app.domain import ID
from app.domain.commands import *
from . import as_started_kookkie
from .route_builder import RouteBuilder
from .http_response_builders import build_response, from_result_of, ok, not_found


class ParticipantRoutes(object):
    @staticmethod
    def with_kookkie_sessions_repository(kookkie_session_repository, jaas_jwt_builder):
        return ParticipantRoutes(join_session=JoinSession(kookkie_session_repository, jaas_jwt_builder))

    def __init__(self, join_session):
        self.join_session = join_session

    def register(self, application):
        route = RouteBuilder(application)

        @route('/api/kookkie-sessions/<kookkie_session_id>/join', methods=['POST'],
               login_required=False)
        @application.csrf.exempt
        def join(kookkie_session_id):
            return build_response(from_result_of(
                self.join_session(ID.from_string(kookkie_session_id)))
                                  .on_failure(404)
                                  .on_success(
                lambda result: (as_started_kookkie(result.started_kookkie), 201)))

        return route



