from quiltz.domain import Success

from app.domain.repositories import InMemoryKookRepository
from app.domain.clock import FixedClock
from app.domain.dummy_context import DummyContext
from app.domain.messenger import MessengerFactory
from app.domain.password_hasher import PasswordHasher
from quiltz.domain.id.testbuilders import aValidID
from testing import *
from app.domain.commands import AcceptTermsOfService
from domain.builders import aValidKook
from quiltz.domain.results import Failure
from support.log_collector import log_collector


