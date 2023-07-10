from flask_migrate import upgrade
from quiltz.messaging.engine.smtp import SMTPBasedMessageEngine

from app import create_app
from app.adapters.metrics import MetricsCollectorCreator
from app.adapters.repositories import AWSBasedSecrets, LocalSecrets, InMemoryKookkieSessionsRepository
from app.adapters.routes import (
    KookkieSessionRoutes,
    ParticipantRoutes,
    KooksRoutes,
    AuthenticationRoutes,
    UserProfileRoutes,
    FlaskLoginBasedCurrentUserRepository,
    VersionRoutes)
from app.domain import MessengerFactory, CountingKookkieSessionRepository
from app.domain.repositories import InMemoryKookRepository
from app.utils.jaas_jwt_builder import JaaSJwtBuilder
from config import Config


def secrets_from_config(config):
    if config.SECRETS_FROM == "aws":
        return AWSBasedSecrets()
    return LocalSecrets(config.SECRETS_FROM)


def main(config=Config,
         kookkie_session_repository=InMemoryKookkieSessionsRepository.with_hard_coded_values(),
         kook_repository=InMemoryKookRepository([]).with_admins(),
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

    ParticipantRoutes.with_kookkie_sessions_repository(counting_kookkie_session_repository, jaas_jwt_builder).register(application)

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
