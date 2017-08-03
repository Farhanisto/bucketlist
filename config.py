import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'precious')
    SQLALCHEMY_DATABASE_URI = 'postgresql://farhanabdi:@localhost/bucketlist'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    BCRYPT_LOG_ROUNDS = 13
    #Flask- settings
    FLASK_SERVER_NAME = "localhost:9999"
    FLASK_DEBUG = True



class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://farhanabdi:@localhost/developbucketlist'
    DEVELOPMENT = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://farhanabdi:@localhost/testbucket'
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4



