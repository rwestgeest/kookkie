from testing import *
from unittest.mock import Mock
from .routes_tests import RoutesTests
from quiltz.domain.results import Success, Failure, PartialSuccess
from app.utils.json_converters import json_loads
from app.adapters.routes.route_builder import RouteBuilder
from app.adapters.routes.http_response_builders import build_response, from_result_of


class TestHttpResponseBuilders(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.my_command = Mock()
        self.my_command.return_value = Success()
        self.setup_app()

    def create_routes(self):
        return MyTestRoute(self.my_command).register(self.application)

    def test_builds_an_ok_when_all_is_ok(self):
        response = self.client.get('/api/my_test_route')
        assert_that(response.status, equal_to('200 OK'))

    def test_builds_an_error_with_a_message_on_failure(self):
        self.my_command.return_value = Failure(message="uh oh")
        response = self.client.get('/api/my_test_route')
        assert_that(response.status, equal_to('400 BAD REQUEST'))
        assert_that(json_loads(response.data), equal_to(dict(message="uh oh")))

    def test_ignores_other_attributes_in_the_failure(self):
        self.my_command.return_value = Failure(message="uh oh", other_attribute="something else")
        response = self.client.get('/api/my_test_route')
        assert_that(json_loads(response.data), equal_to(dict(message="uh oh")))

    def test_builds_an_error_with_a_message_on_partial_success(self):
        self.my_command.return_value = PartialSuccess(message="uh oh")
        response = self.client.get('/api/my_test_route')
        assert_that(response.status, equal_to('400 BAD REQUEST'))
        assert_that(json_loads(response.data), equal_to(dict(message="uh oh")))

    def test_ignores_other_attributes_in_the_partial_success(self):
        self.my_command.return_value = PartialSuccess(message="uh oh", other_attribute="something else")
        response = self.client.get('/api/my_test_route')
        assert_that(json_loads(response.data), equal_to(dict(message="uh oh")))


class MyTestRoute:
    def __init__(self, command):
        self.command = command

    def register(self, application):
        route = RouteBuilder(application)

        @route('/api/my_test_route', methods=['GET'], login_required=False)
        def some_route_root():
            return build_response(from_result_of(self.command()).on_success(lambda result: (dict(), 200)))

        return route