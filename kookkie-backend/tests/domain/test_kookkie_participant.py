from testing import *
from quiltz.domain.id import FixedIDGeneratorGenerating
from quiltz.domain.id.testbuilders import aValidID
from app.domain import (
    KookkieParticipant)

class TestKookkieParticipantGenerate:
    def test_creates_a_participant_with_a_generated_id(self):
        participant = KookkieParticipant.generate(id_generator=FixedIDGeneratorGenerating(aValidID('12'), aValidID('34')))
        assert participant == KookkieParticipant(id=aValidID('12'), joining_id=aValidID('34'))


