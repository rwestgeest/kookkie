from dataclasses import dataclass
from textwrap import dedent


@dataclass
class MessageTemplate:
    subject: str
    body: str


class MessageTemplates:
    invitations = MessageTemplate(
                subject="Invitation to join an Agile Fluency® Diagnostic session",
                body=dedent('''\
                    Hi,

                    You are invited by {kook} to participate in the Agile Fluency® Diagnostic session for team '{team}'. Please use this link to join:
                    
                    {join_link}

                    Kind regards,
                    
                    The Online Agile Fluency Diagnostic Team

                    Privacy Notice:

                    This email was sent by QWAN - Quality Without a Name. You can find our privacy policy, including our contact information, and your rights under the GDPR, at this URL: https://www.qwan.eu/privacy

                    Your email address was provided to us by {kook} specifically for the purpose of sending this invitation. They didn’t give us any other information about you. We deleted your address after sending the invitation, so we can’t use it for anything else.
                    
                    '''))


    @staticmethod
    def invitation(language):
        return MessageTemplates.invitations[language]
