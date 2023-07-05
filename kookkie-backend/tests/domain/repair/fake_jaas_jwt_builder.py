from app.domain import Kook
from app.utils.jaas_jwt_builder import JaaSJwtBuilder

class FakeJaasJwtBuilder(JaaSJwtBuilder):
    def __init__(self):
        super().__init__(None, None, None)
    def for_kook(self, kook: Kook, room: str) -> bytes:
        return f"jwt({kook.name}, {room})".encode()

    def for_guest(self, name, room: str) -> bytes:
        return f"jwt({name}, {room})".encode()

