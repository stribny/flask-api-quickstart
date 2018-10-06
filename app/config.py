import os


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = "VeryVerySecretKey"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_TOKEN_EXPIRATION_DAYS = 30
    AUTH_TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost/flask_api_quickstart"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost/flask_api_quickstart_test"
    )


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
