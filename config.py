import os
from datetime import timedelta

def get_mock_email_config() -> bool:
    MOCK_EMAIL = os.getenv("MOCK_EMAIL")

    #if MOCK_EMAIL env variable is set
    if  MOCK_EMAIL: 
        # MOCK_EMAIL is case insensitive
        MOCK_EMAIL = MOCK_EMAIL.lower()
        
        if MOCK_EMAIL=="true":
            return True
        elif MOCK_EMAIL=="false":
            return False
        else: 
            # if MOCK_EMAIL env variable is set a wrong value
            raise ValueError(
                "MOCK_EMAIL environment variable is optional if set, it has to be valued as either 'True' or 'False'"
            )
    else:
        # Default behaviour is to send the email if MOCK_EMAIL is not set
        return False

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    
    # Flask JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)
    PROPAGATE_EXCEPTION = True

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    
    # mail settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # email authentication
    MAIL_USERNAME = os.getenv("APP_MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("APP_MAIL_PASSWORD")

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    DB_TYPE = os.getenv("DB_TYPE"),
    DB_USERNAME = os.getenv("DB_USERNAME"),
    DB_PASSWORD = os.getenv("DB_PASSWORD"),
    DB_ENDPOINT = os.getenv("DB_ENDPOINT"),
    DB_NAME = os.getenv("DB_NAME")
    DB_TEST_NAME = os.getenv("DB_TEST_NAME")

    @staticmethod
    def build_db_uri(
        db_type_arg = os.getenv("DB_TYPE"),
        db_user_arg = os.getenv("DB_USERNAME"),
        db_password_arg = os.getenv("DB_PASSWORD"),
        db_endpoint_arg = os.getenv("DB_ENDPOINT"),
        db_name_arg = os.getenv("DB_NAME"),
    ):
        return f"{db_type_arg}://{db_user_arg}:{db_password_arg}@{db_endpoint_arg}/{db_name_arg}"
    
    @staticmethod
    def build_db_test_uri(
        db_type_arg = os.getenv("DB_TYPE"),
        db_user_arg = os.getenv("DB_USERNAME"),
        db_password_arg = os.getenv("DB_PASSWORD"),
        db_endpoint_arg = os.getenv("DB_ENDPOINT"),
        db_name_arg = os.getenv("DB_TEST_NAME"),
    ):
        return f"{db_type_arg}://{db_user_arg}:{db_password_arg}@{db_endpoint_arg}/{db_name_arg}"

class LocalConfig(BaseConfig):
    """Local configuration."""

    DEBUG = True

    # Using a local postgre database
    SQLALCHEMY_DATABASE_URI = "postgresql:///bit_schema"
    
    # SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
    
class TestingConfig(BaseConfig):
    TESTING = True
    MOCK_EMAIL = True
    
    # Using a local postgre database
    #SQLALCHEMY_DATABASE_URI = "postgresql:///bit_schema_test"
    
    SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_test_uri()

class StagingConfig(BaseConfig):
    """Staging configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
    

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
    

def get_env_config() -> str:
    flask_config_name = os.getenv("FLASK_ENVIRONMENT_CONFIG", "dev")
    if flask_config_name not in ["prod", "test", "dev", "local", "stag"]:
        raise ValueError(
            "The environment config value has to be within these values: prod, dev, test, local, stag."
        )
    return CONFIGURATION_MAPPER[flask_config_name]

CONFIGURATION_MAPPER = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig",
    "stag": "config.StagingConfig",
    "local": "config.LocalConfig",
    "test": "config.TestingConfig",
}