import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


def getenv_as_bool(variable, default):
    return os.getenv(variable, str(default)) == 'True'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}'.format(path=os.path.join(basedir, 'data', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
    SMTP_PORT = os.getenv('SMTP_PORT', '25')
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    MAIL_FROM = os.getenv('MAIL_FROM', 'no-reply@qwan.eu')
    SECRET_KEY = os.getenv('SECRET_KEY', '@@pn00tm1es')
    FOR_TEST = os.getenv('FOR_TEST', False)
    AWS_CLOUDWATCH = os.getenv('AWS_CLOUDWATCH', False)
    METRICS_HOST = os.getenv('METRICS_HOST', 'localhost')
    METRICS_PORT = os.getenv('METRICS_PORT', 8125)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=720)
    WTF_CSRF_CHECK_DEFAULT = os.getenv('ENABLE_CSRF', True)
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True
    WTF_CSRF_HEADERS = ['X-XSRF-Token']
    SESSION_REFRESH_EACH_REQUEST = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    HTTPS_LINKS=getenv_as_bool('HTTPS_LINKS', True)
    JITSI_APP_ID=os.getenv('JITSI_APP_ID', None)
    JITSI_API_KEY=os.getenv('JITSI_API_KEY', None)
    SECRETS_FROM=os.getenv('SECRETS_FROM', 'aws')
