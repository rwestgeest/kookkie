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

        @route('/api/kookkie-sessions/<kookkie_session_id>/join/<joining_id>', methods=['POST'],
               login_required=False)
        @application.csrf.exempt
        def join(kookkie_session_id, joining_id):
            return build_response(from_result_of(
                self.join_session(ID.from_string(kookkie_session_id), ID.from_string(joining_id)))
                                  .on_failure(404)
                                  .on_success(
                lambda result: (as_joining_info(kookkie_session_id, result.participant,
                                                result.kook_name), 201)))

        return route



def as_joining_info(kookkie_session_id, participant, kook):
    return dict(sessionId=str(kookkie_session_id),
                participantId=str(participant.id),
                kook=kook)

