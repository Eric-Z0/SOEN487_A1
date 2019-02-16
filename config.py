class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///SOEN487_A1.sqlite"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/test_SOEN487_A1.sqlite"