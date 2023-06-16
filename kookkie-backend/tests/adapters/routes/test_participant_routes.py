from testing import *
from app.utils.json_converters import json_dumps, json_loads
from domain.builders import *
from app.domain import *
from app.adapters.routes import *
from .routes_tests import RoutesTests, get_csrf_token


class TestParticipantRoutes_Joining(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app()
        self.participant = KookkieParticipant(id=aValidID('33'), joining_id=aValidID('22'))
        self.join_session.return_value = Success(participant=self.participant, team='Team B', kook_name='Henk')
        
    def create_routes(self):
        self.join_session = Mock()
        return create_participant_routes(join_session=self.join_session).register(self.application)

    def test_calls_the_join_session_command_with_uuids(self):
        self.client.post('/api/kookkie-sessions/{}/join/{}'.format(str(aValidID(11)), str(aValidID(22))))
        self.join_session.assert_called_with(aValidID(11), aValidID(22))

    def test_returns_kook_when_joining(self):
        response = self.client.post('/api/kookkie-sessions/{}/join/{}'.format(str(aValidID(11)), str(aValidID(22))))
        assert response.status == '201 CREATED'
        assert json_loads(response.data) == dict(
            sessionId=str(aValidID('11')), 
            participantId=str(self.participant.id),
            kook='Henk')

    def test_responds_with_error_joining_fails(self):
        self.join_session.return_value = Failure(message='unknown kookkie session')
        response = self.client.post('/api/kookkie-sessions/{}/join/{}'.format(str(aValidID(11)), str(aValidID(22))))
        assert response.status == '404 NOT FOUND'


class TestParticipantRoutes_Joining_CSRF(RoutesTests):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.setup_app(check_csrf=True)
        self.participant = KookkieParticipant(id=aValidID('33'), joining_id=aValidID('22'))
        self.join_session.return_value = Success(participant=self.participant, kook_name='Henk')
        
    def create_routes(self):
        self.join_session = Mock()
        return create_participant_routes(join_session=self.join_session)\
            .register(self.application)

    def test_does_not_check_csrf_on_join(self):
        response = self.client.post('/api/kookkie-sessions/{}/join/{}'.format(str(aValidID(11)), str(aValidID(22))))
        assert response.status == '201 CREATED'

    def test_does_not_issue_csrf_cookie_on_join(self):
        self.client.post('/api/kookkie-sessions/{}/join/{}'.format(str(aValidID(11)), str(aValidID(22))))
        assert get_csrf_token(self.client) is None


def create_participant_routes(**kwargs):
    valid_route_params = dict(join_session=None)
    return ParticipantRoutes(**{**valid_route_params, **kwargs})
