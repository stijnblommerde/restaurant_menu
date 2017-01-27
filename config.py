'''
- separate global configuration from environment specific configurations
- register configurations in config dict
- make configurations safe through environment variables
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MENU_ADMIN = os.environ.get('MENU_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    MAIL_SUBJECT_PREFIX = '[Menu App]'
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_TO = os.environ.get('MAIL_TO')
    SECRET_KEY = 'bla'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data-test.sqlite')
    # disable CSRF tokens in tests
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data.sqlite')


config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig(),

    'default': DevelopmentConfig(),
}