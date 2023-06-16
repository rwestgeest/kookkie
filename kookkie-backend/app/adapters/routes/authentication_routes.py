from flask import jsonify, request, make_response, redirect
from app.domain.commands import ResetPassword, RequestPasswordReset, Signin, Signout
from app.domain.queries import CheckPasswordResetToken
from .http_response_builders import ok
from .route_builder import RouteBuilder, add_csrf
from app.domain import ID


class AuthenticationRoutes:
    @staticmethod
    def create(kook_repository, current_user_repository, message_engine, messenger_factory):
        return AuthenticationRoutes(
            sign_in=Signin(user_repository=kook_repository, current_user_repository=current_user_repository),
            sign_out=Signout(current_user_repository=current_user_repository),
            request_password_reset=RequestPasswordReset(kook_repository, message_engine=message_engine,
                                                        messenger_factory=messenger_factory),
            reset_password=ResetPassword(kook_repository),
            check_reset_password_token=CheckPasswordResetToken(kook_repository))

    def __init__(self, sign_in, sign_out, request_password_reset, reset_password, check_reset_password_token):
        self.request_password_reset = request_password_reset
        self.reset_password = reset_password
        self.check_reset_password_token = check_reset_password_token
        self.sign_in = sign_in
        self.sign_out = sign_out

    def register(self, application):
        route = RouteBuilder(application)

        @route('/api/login', methods=['POST'], login_required=False)
        @application.csrf.exempt
        def login():
            data = request.get_json()
            result = self.sign_in(data['username'], data['password'])
            if result.is_success():
                response = make_response(ok())
                return add_csrf(response)
            if result.blocked:
                return jsonify(messageId='error.authentication.blockedAccount'), 401

            return jsonify(messageId='error.authentication.userNameOrPasswordIncorrect'), 401

        @route('/api/logout', methods=['GET'], login_required=False)
        def sign_out():
            self.sign_out()
            return redirect('/', 302)

        @route('/api/request-password-reset', methods=['POST'], login_required=False)
        @application.csrf.exempt
        def request_reset_password():
            self.request_password_reset(username=request.get_json()['username'],
                                        context=application.front_end_context(request))
            return ok()

        @route('/api/resetpassword/<token>', methods=['GET'], login_required=False)
        def check_reset_password_token(token):
            result = self.check_reset_password_token(token=ID.from_string(token))
            if not result.is_success():
                return jsonify(result.body), 404
            return ok()

        @route('/api/resetpassword', methods=['POST'], login_required=False)
        @application.csrf.exempt
        def reset_password():
            data = request.get_json()
            result = self.reset_password(new_password=data['new_password'], token=ID.from_string(data['token']))
            if not result.is_success():
                return jsonify(result.body), 400
            return ok()

        return route
