import time, uuid
from typing import Dict, Any

from authlib.jose import jwt # type: ignore
from quiltz.domain.id import IDGenerator

from app.domain import Kook


class JaaSJwtBuilder:
    """
        The JaaSJwtBuilder class helps with the generation of the JaaS JWT.
    """

    EXP_TIME_DELAY_SEC = 7200
    # Used as a delay for the exp claim value.

    NBF_TIME_DELAY_SEC = 10

    # Used as a delay for the nbf claim value.

    @classmethod
    def from_config(cls, config, secrets):
        if config.JITSI_API_KEY is None:
            raise "JITSI_API_KEY not configured"
        if config.JITSI_APP_ID is None:
            raise "JITSI_APP_ID not configured"
        return JaaSJwtBuilder(
            app_id=config.JITSI_APP_ID,
            api_key=config.JITSI_API_KEY,
            private_key=secrets.jitsi_private_key
        )


    def __init__(self, app_id, api_key, private_key, id_generator=IDGenerator()) -> None:
        self.header = {'alg': 'RS256'}
        self.userClaims: Dict[str, Any] = {}
        self.featureClaims: Dict[str, Any] = {}
        self.payloadClaims: Dict[str, Any] = {}
        self.id_generator = id_generator
        self.app_id = app_id
        self.api_key = api_key
        self.private_key = private_key

    def withDefaults(self):
        """Returns the JaaSJwtBuilder with default valued claims."""
        return self.withExpTime(int(time.time() + JaaSJwtBuilder.EXP_TIME_DELAY_SEC)) \
            .withNbfTime(int(time.time() - JaaSJwtBuilder.NBF_TIME_DELAY_SEC)) \
            .withLiveStreamingEnabled(False) \
            .withRecordingEnabled(False) \
            .withOutboundCallEnabled(False) \
            .withTranscriptionEnabled(False) \
            .withModerator(False) \
            .withRoomName('*') \
            .withAppID(self.app_id) \
            .withApiKey(self.api_key)

    def withApiKey(self, apiKey):
        """
        Returns the JaaSJwtBuilder with the kid claim(apiKey) set.

        :param apiKey A string as the API Key https://jaas.8x8.vc/#/apikeys
        """
        self.header['kid'] = apiKey
        return self

    def withUserAvatar(self, avatarUrl):
        """
        Returns the JaaSJwtBuilder with the avatar claim set.

        :param avatarUrl A string representing the url to get the user avatar.
        """
        self.userClaims['avatar'] = avatarUrl
        return self

    def withModerator(self, isModerator):
        """
        Returns the JaaSJwtBuilder with the moderator claim set.

        :param isModerator A boolean if set to True, user is moderator and False otherwise.
        """
        self.userClaims['moderator'] = 'true' if isModerator == True else 'false'
        return self

    def withUserName(self, userName):
        """
        Returns the JaaSJwtBuilder with the name claim set.

        :param userName A string representing the user's name.
        """
        self.userClaims['name'] = userName
        return self

    def withUserEmail(self, userEmail):
        """
        Returns the JaaSJwtBuilder with the email claim set.

        :param userEmail A string representing the user's email address.
        """
        self.userClaims['email'] = userEmail
        return self

    def withLiveStreamingEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the livestreaming claim set.

        :param isEnabled A boolean if set to True, live streaming is enabled and False otherwise.
        """
        self.featureClaims['livestreaming'] = 'true' if isEnabled == True else 'false'
        return self

    def withRecordingEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the recording claim set.

        :param isEnabled A boolean if set to True, recording is enabled and False otherwise.
        """
        self.featureClaims['recording'] = 'true' if isEnabled == True else 'false'
        return self

    def withTranscriptionEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the transcription claim set.

        :param isEnabled A boolean if set to True, transcription is enabled and False otherwise.
        """
        self.featureClaims['transcription'] = 'true' if isEnabled == True else 'false'
        return self

    def withOutboundCallEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the outbound-call claim set.

        :param isEnabled A boolean if set to True, outbound calls are enabled and False otherwise.
        """
        self.featureClaims['outbound-call'] = 'true' if isEnabled == True else 'false'
        return self

    def withExpTime(self, expTime):
        """
        Returns the JaaSJwtBuilder with exp claim set. Use the defaults, you won't have to change this value too much.

        :param expTime Unix time in seconds since epochs plus a delay. Expiration time of the JWT.
        """
        self.payloadClaims['exp'] = expTime
        return self

    def withNbfTime(self, nbfTime):
        """
        Returns the JaaSJwtBuilder with nbf claim set. Use the defaults, you won't have to change this value too much.

        :param nbfTime Unix time in seconds since epochs.
        """
        self.payloadClaims['nbfTime'] = nbfTime
        return self

    def withRoomName(self, roomName):
        """
        Returns the JaaSJwtBuilder with room claim set.

        :param roomName A string representing the room to join.
        """
        self.payloadClaims['room'] = roomName
        return self

    def withAppID(self, AppId):
        """
        Returns the JaaSJwtBuilder with the sub claim set.

        :param AppId A string representing the unique AppID (previously tenant).
        """
        self.payloadClaims['sub'] = AppId
        return self

    def withUserId(self, userId):
        """
        Returns the JaaSJwtBuilder with the id claim set.

        :param A string representing the user, should be unique from your side.
        """
        self.userClaims['id'] = userId
        return self

    def for_kook(self, kook: Kook, room: str) -> bytes:
        return self.withDefaults()\
            .withRoomName(room) \
            .withUserName(kook.name) \
            .withUserEmail(kook.email) \
            .withUserId(str(kook.id)) \
            .withModerator(True)\
            .signWith(self.private_key)

    def for_guest(self, name: str, room: str) -> bytes:
        return self.withDefaults()\
            .withRoomName(room) \
            .withUserName(name) \
            .withUserEmail(f"{name}@kookkie.com") \
            .withModerator(False) \
            .withUserId(str(self.id_generator.generate_id()))\
            .signWith(self.private_key)

    def signWith(self, key) -> bytes:
        """
        Returns a signed JWT.

        :param key A string representing the private key in PEM format.
        """
        context = {'user': self.userClaims, 'features': self.featureClaims}
        self.payloadClaims['context'] = context
        self.payloadClaims['iss'] = 'chat'
        self.payloadClaims['aud'] = 'jitsi'
        return jwt.encode(self.header, self.payloadClaims, key)

