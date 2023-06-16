from dataclasses import dataclass


@dataclass(init=False)
class FrontEndContext:
    base_url: str

    def __init__(self, base_url, https=True):
        self.base_url = https and base_url.replace('http://', 'https://') or base_url

    def join_link(self, participant, session_id):
        return '{}join/{}/{}'.format(self.base_url, str(session_id), str(participant.joining_id))

    def password_reset_link(self, kook):
        return '{}reset-password/{}'.format(self.base_url, str(kook.password_reset_token.token))

    def update_email_link(self, email_update_request):
        return '{}api/profile/email/{}'.format(self.base_url, str(email_update_request.token))
