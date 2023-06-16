import pytest
from app.adapters.routes import *
from .routes_tests import RoutesTests
from app.utils.json_converters import json_loads

class TestVersionRoutes_Get(RoutesTests):
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.setup_app()

    def create_routes(self):
        return VersionRoutes.create().register(self.app)

    def test_post_kook_invokes_create_kook_command_with_body_parameters_and_kook(self):
        expected_version = ''
        with open('VERSION') as f: 
            expected_version = f.read().strip()
        response = self.client.get('/api/version', content_type='application/json')
        assert response.status == '200 OK'
        assert json_loads(response.data) == dict(version=expected_version)
