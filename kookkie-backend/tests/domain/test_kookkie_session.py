from domain.repair.fake_jaas_jwt_builder import FakeJaasJwtBuilder
from testing import *
from quiltz.domain.id import FixedIDGeneratorGenerating
from domain.builders import *


class TestCreateWithId:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.id_generator = FixedIDGeneratorGenerating(aValidID('12'))
        self.clock = Clock.fixed()
        self.creator = KookkieSessionCreator(id_generator = self.id_generator, clock=self.clock)

    def test_creates_an_event_with_a_timestamp(self):
        event = self.creator.create_with_id(date="date", participant_count='2',
                                            kook=aValidKook()).kookkie_session_created
        assert event.timestamp == self.clock.now()

    def test_creates_a_kookkie_session_with_a_generated_id(self):
        kookkie_session = self.creator.create_with_id(date="date", participant_count='2',
                                                         kook=aValidKook()).kookkie_session_created.kookkie_session
        assert kookkie_session.id == aValidID('12')

    def test_assigns_all_other_attributes(self):
        kookkie_session = self.creator.create_with_id(
            date="date",
            participant_count='10',
            kook=aValidKook()).kookkie_session_created.kookkie_session
        assert kookkie_session.date == "date"
        assert kookkie_session.kook_id == aValidID('100')
        assert kookkie_session.kook_name == 'F. Kook'

    def test_fails_when_date_is_not_present(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(date=None)) == Failure(message='date is missing')

    def test_fails_when_participant_count_is_not_present(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count=None)) == Failure(message='participant_count is missing')

    def test_fails_when_participant_count_is_not_an_integer(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count='bla')) == Failure(message='participant_count is not an integer value')

    def test_fafils_when_participant_count_is_more_than_30(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count='31')) == Failure(message='participant_count should be between 1 and 30')

    def test_fails_when_participant_count_is_less_than_1(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count='-1')) == Failure(message='participant_count should be between 1 and 30')

    def test_fails_when_kook_is_not_present(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(kook=None)) == Failure(message='kook is missing')


class TestEquality:
    def test_returns_true_if_ids_are_equal(self):
        assert aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111")) == aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111"))

    def test_returns_false_if_ids_are_not_equal(self):
        assert aValidKookkieSession(id=ID.from_string("22222222222222222222222222222222")) != aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111"))

    def test_returns_false_if_other_is_none(self):
        assert aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111")) is not None

    def test_returns_false_if_other_is_not_a_kookkie_session(self):
        assert aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111")) != SomeObj(id=ID.from_string("11111111111111111111111111111111"))

class TestAsListItem:
    def test_as_list_item_returns_a_list_item_with_id_name_date_and_kookkie_name(self):
        kookkie= aValidKookkieSession()
        list_item = kookkie.as_list_item()
        assert_that(list_item, equal_to(KookkieSessionListItem(
            id=kookkie.id,
            date=kookkie.date,
            kook_name=kookkie.kook_name,
            name=kookkie.name
        )))

class TestStart:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.jwt_builder = FakeJaasJwtBuilder()
        self.kookkie_session = aValidKookkieSession(kook_id=aValidID('100'))

    def test_creates_started_kookkie_session(self):
        kook = aValidKook(id=aValidID('100'))
        result = self.kookkie_session.start(kook, self.jwt_builder)
        assert_that(result, equal_to(Success(started_kookkie=self.jwt_builder.join_info_for_kook(kook, self.kookkie_session))))

    def test_fails_when_kook_not_the_kook_of_this_session(self):
        kook = aValidKook(id=aValidID('999'))
        result = self.kookkie_session.start(kook, self.jwt_builder)
        assert_that(result, equal_to(Failure(message="This is not your kookkie")))


class TestJoin:
    def test_creates_a_started_kookkie_session_for_the_guest(self):
        jwt_builder = FakeJaasJwtBuilder()
        kookkie_session = aValidKookkieSession()
        result = kookkie_session.join("harry", jwt_builder)
        assert_that(result, equal_to(Success(started_kookkie=jwt_builder.join_info_for_guest("harry", kookkie_session))))


class TestRoomName:
    def test_is_camelized_description(self):
        kookkie = aValidKookkieSession(name="lekker eten")
        assert_that(kookkie.room_name, equal_to("LekkerEten"))
    def test_skips_tabs(self):
        kookkie = aValidKookkieSession(name="lekker\teten")
        assert_that(kookkie.room_name, equal_to("LekkerEten"))

class SomeObj(object):
    def __init__(self, id):
        self.id = id


