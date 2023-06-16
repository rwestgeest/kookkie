#!/usr/bin/env python
import sys
sys.path.append('.')
from app.domain import MessengerFactory, DummyContext
from domain.builders import aValidKook, aValidKookMessage
from quiltz.messaging.engine.smtp import SMTPBasedMessageEngine, as_smtp_message

class Config:
    SMTP_HOST = 'email-smtp.eu-central-1.amazonaws.com'
    SMTP_PORT = '587'
    FOR_TEST  = False
    MAIL_FROM = 'no-reply@qwan.eu'
    SMTP_USER=''
    SMTP_PASSWORD=''

remote_secrets={}
with open('../donstro/remote.secrets') as f:
    remote_secrets = { k:v for (k,v) in [ line.strip().split('=') for line in f.readlines() ]}

Config.SMTP_USER=remote_secrets['SMTP_USER']
Config.SMTP_PASSWORD=remote_secrets['SMTP_PASSWORD']

message_engine = SMTPBasedMessageEngine.from_config(Config)
messenger = MessengerFactory.from_config(Config).create(DummyContext())
messenger.send(aValidKookMessage(to=aValidKook(email="marc.evers@gmail.com", name='Märc'), sender=Config.MAIL_FROM, subject="Hi Kook", body='My message'))
print(message_engine.commit(messenger))