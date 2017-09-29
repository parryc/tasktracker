import os

class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'guadalupe-hidalgo'
#    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/task'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///tasks'
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_DISABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    CSRF_ENABLED = False
    SECRET_KEY = 'guadalupe-hidalgo-testing-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'   # + os.path.join(basedir, 'test.db')
    SQLALCHEMY_RECORD_QUERIES = False
    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    # From RealPython tutorial
    # https://realpython.com/blog/python/python-web-applications-with-flask-part-iii/
    HASH_ROUNDS = 1

# Only use in case of postgres specific functions, like regex matching
class PostgresTestingConfig(Config):
    TESTING = True
    CSRF_ENABLED = False
    SECRET_KEY = 'guadalupe-hidalgo-testing-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test_tasks'
    HASH_ROUNDS = 1
