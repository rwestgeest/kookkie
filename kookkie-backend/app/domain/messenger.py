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
            subject='Welcome to the online Agile Fluency® Diagnostic',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                Welcome to the online Agile Fluency® Diagnostic.

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
            subject='Password reset for the online Agile Fluency® Diagnostic',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                You have requested to reset your password for the online Agile Fluency® Diagnostic.

                Please use this link to set your password:

                {reset_link}

                This link will be valid for {password_expiry} minutes.

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(reset_link=context.password_reset_link(kook),
                           name=kook.name,
                           password_expiry=str(PasswordResetToken.PASSWORD_RESET_EXPIRY_IN_MINUTES))))

    @staticmethod
    def invitation(participant, sender, email, kookkie_session, context):
        message_template = MessageTemplates.invitation(kookkie_session.language)
        return Message.for_unnamed_recipient(
            to=email,
            subject=message_template.subject,
            sender=sender,
            body=message_template.body.format(
                    join_link=context.join_link(participant, kookkie_session.id),
                    kook=kookkie_session.kook_name,
                    team=kookkie_session.team)
            )

    @staticmethod
    def email_update_notification(kook, sender): 
        return Message.for_named_recipient(
            to=kook,
            subject='A request to update your email address has been received for the online Agile Fluency® Diagnostic',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                We have received a request to change your email address for the online Agile Fluency® Diagnostic.

                If you have not requested this, please contact the Agile Fluency Project at:
                https://www.agilefluency.org/contact.php

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(name=kook.name)))

    @staticmethod
    def email_update_message(kook, email_update_request, sender):
        return Message.for_unnamed_recipient(
            to=email_update_request.new_email,
            subject='Confirm your new email address for the online Agile Fluency® Diagnostic',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                Please use this code to confirm your new email address:

                {confirmation_code}

                This code will be valid for {expiry} minutes.

                If you have not requested this, please contact the Agile Fluency Project at:
                https://www.agilefluency.org/contact.php

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(name=kook.name, confirmation_code=email_update_request.code, expiry=str(EmailUpdateRequest.EXPIRY_IN_MINUTES))))
                
    @staticmethod
    def email_updated_notification(kook, old_email, sender):
        return Message.for_unnamed_recipient(
            to=old_email,
            subject='Your email address has been updated for the online Agile Fluency® Diagnostic',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                Your email address has been updated for the online Agile Fluency® Diagnostic. You are no longer able to sign in using {email}.

                If you have not requested this, please contact the Agile Fluency Project at:
                https://www.agilefluency.org/contact.php

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(name=kook.name, email=old_email)))

    @staticmethod
    def email_updated_confirmation(kook, sender):
        return Message.for_named_recipient(
            to=kook,
            subject='Your email address has been updated for the online Agile Fluency® Diagnostic',
            sender=sender,
            body=dedent('''\
                Hello {name},
          
                Your email address has been updated for the online Agile Fluency® Diagnostic.

                Kind regards,

                The Online Agile Fluency Diagnostic Team
                '''.format(name=kook.name)))


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

    def send_invitation(self, participant, email, kookkie_session):
        self.logger.info("Sending kookkie session invitation to {}".format(anonymize(email)))
        return self.send(Messages.invitation(participant=participant, email=email, sender=self.sender,
                                             kookkie_session=kookkie_session, context=self.context))

    def send_email_update_notification(self, kook):
        return self.send(Messages.email_update_notification(kook, sender=self.sender))

    def send_email_update_message(self, kook, email_update_request):
        return self.send(Messages.email_update_message(kook, email_update_request, sender=self.sender))

    def send_email_updated_notification(self, kook, old_email):
        return self.send(Messages.email_updated_notification(kook, old_email, sender=self.sender))

    def send_email_updated_confirmation(self, kook):
        return self.send(Messages.email_updated_confirmation(kook, sender=self.sender))


class MessengerFactory:
    @staticmethod
    def from_config(config):
        return MessengerFactory(sender=config.MAIL_FROM)

    def __init__(self, sender="noreply@agilefluency.org"):
        self.sender = sender
        
    def create(self, context):
        return Messenger(sender=self.sender, context=context)
