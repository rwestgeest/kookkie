#!/usr/bin/env python
import sys

from flask_migrate import migrate

from app import create_app
from app.adapters.repositories import DBKookkieSessionsRepository, DBKookRepository
from config import Config

message = ' '.join(sys.argv[1:])

if not message:
    print('Please provide a migration message')
    exit(-1)

kookkie_session_repository = DBKookkieSessionsRepository()
kook_repository = DBKookRepository()

application = create_app(Config)

with application.app_context():
    migrate(directory='migrations', message=message)
