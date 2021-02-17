import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or "postgres://postgres:postgres@localhost:5432/genome_sequencer"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    CORS_HEADERS = "Content-Type"


class StagingConfig(Config):
    ENV = "staging"
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
