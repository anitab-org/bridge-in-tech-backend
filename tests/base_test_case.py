from flask_testing import TestCase

from app.database.models.ms_schema.user import UserModel
from run import application
from app.database.sqlalchemy_extension import db

from tests.test_data import test_admin_user


class BaseTestCase(TestCase):
    @classmethod
    def create_app(cls):
        application.config.from_object("config.TestingConfig")

        # Setting up test environment variables
        application.config["SECRET_KEY"] = "TEST_SECRET_KEY"
        application.config["SECURITY_PASSWORD_SALT"] = "TEST_SECURITY_PWD_SALT"
        return application

    def setUp(self):
        
        db.create_all()


    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        