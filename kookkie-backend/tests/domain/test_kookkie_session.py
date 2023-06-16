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
        assert kookkie_session.participant_count() == 10
        assert kookkie_session.kook_id == aValidID('100')
        assert kookkie_session.kook_name == 'F. Kook'

    def test_generates_participant_count_participants_with_an_id_and_a_color(self):
        kookkie_session = self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count=2)).kookkie_session_created.kookkie_session
        assert kookkie_session.participants == [ 
            KookkieParticipant.generate(id_generator=self.id_generator),
            KookkieParticipant.generate(id_generator=self.id_generator)
            ]

    def test_fails_when_date_is_not_present(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(date=None)) == Failure(message='date is missing')

    def test_fails_when_participant_count_is_not_present(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count=None)) == Failure(message='participant_count is missing')

    def test_fails_when_participant_count_is_not_an_integer(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count='bla')) == Failure(message='participant_count is not an integer value')

    def test_fails_when_participant_count_is_more_than_30(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count='31')) == Failure(message='participant_count should be between 1 and 30')

    def test_fails_when_participant_count_is_less_than_1(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(participant_count='-1')) == Failure(message='participant_count should be between 1 and 30')

    def test_fails_when_kook_is_not_present(self):
        assert self.creator.create_with_id(**validKookkieSessionCreationParameters(kook=None)) == Failure(message='kook is missing')



class TestJoinSession:
    def test_responds_with_error_when_participant_not_found_in_session(self):
        kookkie_session = aValidKookkieSession(participants=[])
        assert kookkie_session.join_participant_by_id(aValidID(22)) == UNKNOWN_PARTICIPANT
    
    def test_returns_success_when_joining(self):
        participant = KookkieParticipant(id=aValidID('33'), joining_id=aValidID('22'))
        kookkie_session = aValidKookkieSession(participants=[participant],
                                                     kook_name='Mr. Kook')
        assert kookkie_session.join_participant_by_id(aValidID(22)) == Success(
            participant=participant, kook_name='Mr. Kook')


class TestEquality:
    def test_returns_true_if_ids_are_equal(self):
        assert aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111")) == aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111"))

    def test_returns_false_if_ids_are_not_equal(self):
        assert aValidKookkieSession(id=ID.from_string("22222222222222222222222222222222")) != aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111"))

    def test_returns_false_if_other_is_none(self):
        assert aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111")) is not None

    def test_returns_false_if_other_is_not_a_kookkie_session(self):
        assert aValidKookkieSession(id=ID.from_string("11111111111111111111111111111111")) != SomeObj(id=ID.from_string("11111111111111111111111111111111"))


class TestAddingParticipants:
    def test_adds_new_participant(self):
        session = aValidKookkieSession(participants=[])
        result = session.add_participant(FixedIDGeneratorGenerating(aValidID('12')))
        assert_that(result, equal_to(Success(
            event=ParticipantWasAdded(kookkie_session=session,
                                      new_participant=aValidKookkieParticipant(id=aValidID('12'),
                                                                               joining_id=aValidID('12'),
                                                                               email='')))))
        assert_that(session.participant_count(), equal_to(1))

    def test_does_not_add_participants_beyond_maximum(self):
        session = aValidKookkieSession(participants=[aValidKookkieParticipant() for i in range(30)])
        result = session.add_participant()
        assert_that(session.participant_count(), equal_to(30))
        assert_that(result, equal_to(Failure(message='Cannot have more than 30 participants')))
        

class SomeObj(object):
    def __init__(self, id):
        self.id = id


