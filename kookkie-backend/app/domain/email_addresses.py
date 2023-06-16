from quiltz.domain.id import ID
from dataclasses import dataclass, field
from typing import List


@dataclass
class EmailAddress:
    email: str
    participant_id: ID


@dataclass
class EmailAddresses:
    email_addresses: List[EmailAddress] = field(default_factory=list)

    @staticmethod
    def from_data(data) -> 'EmailAddresses':
        return EmailAddresses([
            EmailAddress(participant['email'], ID.from_string(participant['participant_id']))
            for participant in data['email_addresses']
        ])
