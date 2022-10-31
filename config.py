"""Flask app configuration."""
from os import environ, path

import redis
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Assets
    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")

    # Flask-Session
    REDIS_URI = environ.get("SESSION_REDIS")

    # null: NullSessionInterface(default)
    # redis: RedisSessionInterface
    # memcached: MemcachedSessionInterface
    # filesystem: FileSystemSessionInterface
    # mongodb: MongoDBSessionInterface
    # sqlalchemy: SqlAlchemySessionInterface
    ##
    # SESSION_TYPE = "filesystem"
    ##
    MY_GMAIL = environ.get("MY_GMAIL")
    MY_OUTLOOK = environ.get("MY_OUTLOOK")

    SENDER_EMAIL = environ.get("SENDER_EMAIL")
    RECEIVER_EMAIL = environ.get("RECEIVER_EMAIL")

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(REDIS_URI)
