from quiltz.domain.id.testbuilders import aValidID
from domain.builders import aValidKookkieParticipant, aValidKook, aValidPasswordResetToken
from app.domain import FrontEndContext


class TestFrontendContext:
    def test_join_link_concatenates_the_sesion_id_and_joining_id_with_prefix(self):
        participant = aValidKookkieParticipant(joining_id=aValidID('34'))
        assert FrontEndContext('the_prefix/').join_link(participant, aValidID('99')) == 'the_prefix/join/{}/{}'.format(aValidID('99'), aValidID('34'))

    def test_password_reset_link_concatenates_token_with_prefix(self):
        kook = aValidKook(password_reset_token=aValidPasswordResetToken(aValidID("101")))
        assert FrontEndContext('the_prefix/').password_reset_link(kook) == 'the_prefix/reset-password/{}'.format(aValidID('101'))

    def test_link_replaces_http_by_https(self):
        kook = aValidKook(password_reset_token=aValidPasswordResetToken(aValidID("101")))
        assert FrontEndContext('http://qwan.eu/', https=True).password_reset_link(kook) == 'https://qwan.eu/reset-password/{}'.format(aValidID('101'))

    def test_link_keeps_http_when_https_is_false(self):
        participant = aValidKookkieParticipant(joining_id=aValidID('34'))
        assert FrontEndContext('http://qwan.eu/', https=False).join_link(participant, aValidID('99')) == 'http://qwan.eu/join/{}/{}'.format(aValidID('99'), aValidID('34'))
