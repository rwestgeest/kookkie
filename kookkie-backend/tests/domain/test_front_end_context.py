from quiltz.domain.id.testbuilders import aValidID
from domain.builders import aValidKookkieParticipant, aValidKook, aValidPasswordResetToken
from app.domain import FrontEndContext


class TestFrontendContext:
    def test_password_reset_link_concatenates_token_with_prefix(self):
        kook = aValidKook(password_reset_token=aValidPasswordResetToken(aValidID("101")))
        assert FrontEndContext('the_prefix/').password_reset_link(kook) == 'the_prefix/reset-password/{}'.format(aValidID('101'))

    def test_link_replaces_http_by_https(self):
        kook = aValidKook(password_reset_token=aValidPasswordResetToken(aValidID("101")))
        assert FrontEndContext('http://qwan.eu/', https=True).password_reset_link(kook) == 'https://qwan.eu/reset-password/{}'.format(aValidID('101'))

