from dataclasses import dataclass


@dataclass
class DummyContext:
    def join_link(self, participant, session_id):
        return 'join-link-{}'.format(participant.id)

    def password_reset_link(self, kook):
        return 'reset-password'
    
    def update_email_link(self, request):
        return 'update-email'
