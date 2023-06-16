from flask_login import login_required
from flask_wtf.csrf import generate_csrf


class RouteBuilder:
    XSRF_COOKIE_NAME = 'XSRF-TOKEN'

    def __init__(self, app):
        self.app = app
        self.unspecified_logins = []

    def __call__(self, rule, **options):
        login_required_option = options.pop('login_required', None)
        methods = options.get('methods')
        if login_required_option is None:
            self.unspecified_logins.append("{methods}: {rule}".format(methods=', '.join(methods), rule=rule))

        def route_wrapper(f):
            return self.app.route(rule, **options)(f)

        def login_wrapper(f):
            return route_wrapper(login_required(f))
        
        if login_required_option:
            return login_wrapper
        else:
            return route_wrapper    


def add_csrf(response):
    response.set_cookie(RouteBuilder.XSRF_COOKIE_NAME, generate_csrf(), samesite='strict')
    return response
