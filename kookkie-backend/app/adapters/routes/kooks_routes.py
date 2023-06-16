from app.domain.commands.kook_commands import ToggleRole
from flask import request
from app.domain.commands import CreateKook
from app.domain.queries import AllKooks, AllKookSessionCounts
from .route_builder import RouteBuilder
from .http_response_builders import build_response, from_result_of
from app.domain import ID, Clock, Kook


class KooksRoutes:
    @staticmethod
    def create(kooks_repository, kookkie_session_repository, current_user_repository, message_engine, messenger_factory):
        return KooksRoutes(
            current_user_repository=current_user_repository,
            create=CreateKook(kooks_repository, message_engine, messenger_factory=messenger_factory),
            all=AllKooks(kooks_repository),
            kook_session_counts=AllKookSessionCounts(kookkie_session_repository))

    def __init__(self, current_user_repository, create, all, kook_session_counts):
        self.authenticator = current_user_repository
        self.create_kook = create
        self.all_kook = all
        self.kook_session_counts = kook_session_counts

    def register(self, application):
        route = RouteBuilder(application)

        @route('/api/kooks', methods=['POST'], login_required=True)
        def create_kook():
            return build_response(from_result_of(
                self.create_kook(
                    request.json,
                    context=application.front_end_context(request),
                    user=self.authenticator.current_user()))
                .on_success(lambda result: (dict(id=str(result.id)), 201)))

        @route('/api/kooks', methods=['GET'], login_required=True)
        def get_kooks():
            return build_response(from_result_of(self.all_kook(user=self.authenticator.current_user()))
                    .on_success(lambda result: (as_kook_list(result.kooks), 200))
                    .with_csrf())

        @route('/api/kooks-session-counts', methods=['GET', 'POST'], login_required=True)
        def session_counts():
            since = request.method == 'POST' and request.json and Clock().parse_date(request.json['since']) or None
            return build_response(
                from_result_of(self.kook_session_counts(user=self.authenticator.current_user(), since=since))
                .on_success(lambda result: (as_counts_list(result.counts), 200)))

        return route

def as_kook_list(kooks: list[Kook]):
    return dict(kooks=list(map(as_kook, kooks)))

def as_kook(kook: Kook):
    result = dict(id=str(kook.id), name=kook.name, email=kook.email,
                  isAdmin=kook.is_admin)
    return result


def as_counts_list(kook_counts):
    return dict(kook_session_counts = [dict(id=str(f.id), name=f.name, count=f.count) for f in kook_counts.counts])
