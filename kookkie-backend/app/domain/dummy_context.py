from dataclasses import dataclass


@dataclass
class DummyContext:
    def password_reset_link(self, kook):
        return 'reset-password'
    
    def update_email_link(self, request):
        return 'update-email'
