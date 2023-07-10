from quiltz.messaging.messenger import Message, Messenger as QuiltzMessenger
from app.domain import PasswordResetToken, anonymize
from .message_templates import MessageTemplates
from .dummy_context import DummyContext
from textwrap import dedent
import logging


class Messages:
    @staticmethod
    def welcome(kook, sender, context):
        return Message.for_named_recipient(
            to=kook,
            subject='Welcome to Kookkie',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                Welcome to Kookkie.

                Please use this link to set your password:

                {reset_link}

                This link will be valid for {initial_password_expiry} hours.

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(reset_link=context.password_reset_link(kook),
                           name=kook.name,
                           initial_password_expiry=str(PasswordResetToken.INITIAL_PASSWORD_EXPIRY_IN_MINUTES // 60))))

    @staticmethod
    def password_reset(kook, sender, context):
        return Message.for_named_recipient(
            to=kook,
            subject='Password reset for Kookkie',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                You have requested to reset your password for Kookkie.

                Please use this link to set your password:

                {reset_link}

                This link will be valid for {password_expiry} minutes.

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(reset_link=context.password_reset_link(kook),
                           name=kook.name,
                           password_expiry=str(PasswordResetToken.PASSWORD_RESET_EXPIRY_IN_MINUTES))))


class Messenger(QuiltzMessenger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def for_test():
        return Messenger('sender@mail.com', DummyContext())

    def send_welcome(self, kook):
        self.logger.info("Sending welcome message to {}".format(anonymize(kook.email)))
        return self.send(Messages.welcome(kook, sender=self.sender, context=self.context))

    def send_password_reset(self, kook):
        self.logger.info("Sending password reset message to {}".format(anonymize(kook.email)))
        return self.send(Messages.password_reset(kook, sender=self.sender, context=self.context))


class MessengerFactory:
    @staticmethod
    def from_config(config):
        return MessengerFactory(sender=config.MAIL_FROM)

    def __init__(self, sender="noreply@agilefluency.org"):
        self.sender = sender
        
    def create(self, context):
        return Messenger(sender=self.sender, context=context)
