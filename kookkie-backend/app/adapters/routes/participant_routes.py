from flask import jsonify, request
from app.domain import ID
from app.domain.commands import *
from .route_builder import RouteBuilder
from .http_response_builders import build_response, from_result_of, ok, not_found


class ParticipantRoutes(object):
    @staticmethod
    def with_kookkie_sessions_repository(kookkie_session_repository):
        return ParticipantRoutes(join_session=JoinSession(kookkie_session_repository))

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
                lambda result: (as_joining_info(result.kookkie_session), 201)))

        return route



def as_joining_info(kookkie_session):
    return dict(id=str(kookkie_session.id), date=kookkie_session.date,
                      kook_name=kookkie_session.kook_name)

