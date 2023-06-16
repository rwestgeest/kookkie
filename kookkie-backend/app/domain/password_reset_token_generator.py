from app.domain.clock import Clock
from quiltz.domain.id import IDGenerator
from .password_reset_token import PasswordResetToken


class PasswordResetTokenGenerator:
    def __init__(self, id_generator=IDGenerator()):
        self.id_generator=id_generator

    def generate_token(self):
        return PasswordResetToken.create_password_reset_token(self.id_generator.generate_id(), Clock().now())

    def generate_initial_token(self):
        return PasswordResetToken.create_initial_password_token(self.id_generator.generate_id(), Clock().now())
    
    def from_id(self, id_instance):
        return PasswordResetToken.create_password_reset_token(id_instance, Clock().now())


class FixedPasswordTokenGeneratorGenerating(PasswordResetTokenGenerator):
    def __init__(self, password_reset_token):
        self._the_token_to_generate=password_reset_token    

    def generate_token(self):
        return self._the_token_to_generate


class FixedInitialPasswordTokenGeneratorGenerating(PasswordResetTokenGenerator):
    def __init__(self, password_reset_token):
        self._the_token_to_generate=password_reset_token    

    def generate_initial_token(self):
        return self._the_token_to_generate


class PasswordTokenGeneratorGeneratingWithTimeStamp:
    def __init__(self, created_time):
        self._created_time=created_time

    def from_id(self, id_instance):
        return PasswordResetToken.create_password_reset_token(token=id_instance, created_time=self._created_time)
