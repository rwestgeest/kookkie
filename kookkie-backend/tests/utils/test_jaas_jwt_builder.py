from typing import Dict

from authlib.jose import jwt, JWTClaims  # type: ignore

from app.utils.jaas_jwt_builder import JaaSJwtBuilder
from domain.builders import aValidKook
from quiltz.domain.id import FixedIDGeneratorGenerating
from quiltz.domain.id.testbuilders import aValidID
from testing import *

class AbstractJaasJwtTest:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.app_id = "my_app_id"
        self.api_key = "api_key"
        self.room_name = "kamertje"
        self.jassJwt: JaaSJwtBuilder = JaaSJwtBuilder(
            app_id=self.app_id,
            api_key=self.api_key,
            private_key=private_key(),
            id_generator=FixedIDGeneratorGenerating(aValidID("22"))
        )

    def test_contains_no_special_features_at_all(self):
        claims = claims_in(self.generate_jwt())
        assert_that(claims["context"]["features"], equal_to({
            'livestreaming': 'false',
            'recording': 'false',
            'outbound-call': 'false',
            'transcription': 'false'
        }))

    def test_contains_app_id(self):
        claims = claims_in(self.generate_jwt())
        assert_that(claims['sub'], equal_to(self.app_id))

    def test_contains_api_key(self):
        headers = headers_in(self.generate_jwt())
        assert_that(headers['kid'], equal_to(self.api_key))

    def test_contains_room_name(self):
        claims = claims_in(self.generate_jwt())
        assert_that(claims['room'], equal_to(self.room_name))

    def generate_jwt(self):
        pass


class TestJaasJwtGenerationForKook(AbstractJaasJwtTest):
    __test__ = True

    def generate_jwt(self) -> bytes:
        return self.jassJwt.for_kook(aValidKook(), room=self.room_name)

    def test_makes_it_host_with_user_and_email(self):
        claims = claims_in(self.generate_jwt())
        assert_that(claims['context']['user'], equal_to(dict(
            moderator = 'true',
            name = aValidKook().name,
            email = aValidKook().email,
            id = str(aValidKook().id),
        )))

class TestJaasJwtGenerationForGuest(AbstractJaasJwtTest):
    __test__ = True

    def generate_jwt(self) -> bytes:
        return self.jassJwt.for_guest("harry", room=self.room_name)

    def test_for_guest_makes_it_guest_with_user_and_email(self):
        claims = claims_in(self.generate_jwt())
        assert_that(claims['context']['user'], equal_to(dict(
            moderator = 'false',
            name = "harry",
            email = "harry@kookkie.com",
            id = str(aValidID(22)),
        )))


def claims_in(jass_jwt: bytes) -> JWTClaims:
    return decode(jass_jwt)


def headers_in(jass_jwt: bytes) -> Dict[str, str]:
    return claims_in(jass_jwt).header


def decode(token: bytes):
    return jwt.decode(token, public_key())


def sign(jassJwt: JaaSJwtBuilder) -> bytes:
    return jassJwt.signWith(private_key())


def private_key():
    with open("tests/data/jassauth.test.key") as f:
        return f.read()


def public_key():
    with open("tests/data/jassauth.test.key.pub") as f:
        return f.read()
