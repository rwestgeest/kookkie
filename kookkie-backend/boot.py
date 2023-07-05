from app import create_app
from app.adapters.routes import (
    KookkieSessionRoutes,
    ParticipantRoutes,
    KooksRoutes,
    AuthenticationRoutes,
    UserProfileRoutes,
    FlaskLoginBasedCurrentUserRepository,
    VersionRoutes)
from app.domain import MessengerFactory, CountingKookkieSessionRepository
from app.utils.jaas_jwt_builder import JaaSJwtBuilder
from config import Config
from app.adapters.repositories import DBKookkieSessionsRepository, DBKookRepository, AWSBasedSecrets, LocalSecrets
from app.adapters.metrics import MetricsCollectorCreator
from quiltz.messaging.engine.smtp import SMTPBasedMessageEngine
from flask_migrate import upgrade

def secrets_from_config(config):
    match config.SECRETS_FROM:
        case "aws":
            return AWSBasedSecrets()
        case "local":
            return LocalSecrets()
        case _:
            raise "No Secrets configured"

def main(config=Config,
         kookkie_session_repository=DBKookkieSessionsRepository(),
         kook_repository=DBKookRepository(),
         metricsCollectorCreator=MetricsCollectorCreator.forProd()):

    application = create_app(config)

    with application.app_context():
        upgrade()
        kook_repository = kook_repository.with_admins()

    message_engine = SMTPBasedMessageEngine.from_config(config)
    messenger_factory = MessengerFactory.from_config(config)

    secrets = secrets_from_config(config)
    jaas_jwt_builder = JaaSJwtBuilder.from_config(config, secrets)

    current_user_repository = FlaskLoginBasedCurrentUserRepository(kook_repository).register(application.app)

    counting_kookkie_session_repository = CountingKookkieSessionRepository(
        kookkie_session_repository,
        metricsCollectorCreator.create_collector(config))

    KookkieSessionRoutes.with_kookkie_sessions_repository(
        counting_kookkie_session_repository,
        current_user_repository=current_user_repository,
        jaas_jwt_builder=jaas_jwt_builder
    ).register(application)

    ParticipantRoutes.with_kookkie_sessions_repository(counting_kookkie_session_repository).register(application)

    AuthenticationRoutes.create(
        kook_repository,
        current_user_repository=current_user_repository,
        message_engine=message_engine,
        messenger_factory=messenger_factory).register(application)

    KooksRoutes.create(kooks_repository=kook_repository, kookkie_session_repository=kookkie_session_repository,
                       current_user_repository=current_user_repository, message_engine=message_engine,
                       messenger_factory=messenger_factory).register(application)
    UserProfileRoutes.create(current_user_repository=current_user_repository).register(application)
    VersionRoutes.create().register(application)
    return application.app
