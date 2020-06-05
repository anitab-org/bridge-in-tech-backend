import os
from flask import Flask, jsonify

# from flask_restx import Resource, Api
from config import get_env_config
from flask_migrate import Migrate, MigrateCommand


def create_app(config_filename: str) -> Flask:
    # instantiate the app
    app = Flask(__name__, instance_relative_config=True)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    from app.database.sqlalchemy_extension import db

    db.init_app(app)

    from app.database.models.ms_schema.user import UserModel
    from app.database.models.ms_schema.mentorship_relation import (
        MentorshipRelationModel,
    )
    from app.database.models.ms_schema.tasks_list import TasksListModel
    from app.database.models.ms_schema.task_comment import TaskCommentModel
    from app.database.models.bit_schema.organization import OrganizationModel
    from app.database.models.bit_schema.program import ProgramModel
    from app.database.models.bit_schema.user_extension import UserExtensionModel
    from app.database.models.bit_schema.personal_background import (
        PersonalBackgroundModel,
    )
    from app.database.models.bit_schema.mentorship_relation_extension import (
        MentorshipRelationExtensionModel,
    )

    migrate = Migrate(app, db)

    from app.api.jwt_extension import jwt

    jwt.init_app(app)

    from app.api.bit_extension import api

    api.init_app(app)

    from app.api.mail_extension import mail

    mail.init_app(app)

    return app


application = create_app(get_env_config())


@application.before_first_request
def create_tables():
    from app.database.sqlalchemy_extension import db

    from app.database.models.ms_schema.user import UserModel
    from app.database.models.ms_schema.mentorship_relation import (
        MentorshipRelationModel,
    )
    from app.database.models.ms_schema.tasks_list import TasksListModel
    from app.database.models.ms_schema.task_comment import TaskCommentModel
    from app.database.models.bit_schema.organization import OrganizationModel
    from app.database.models.bit_schema.program import ProgramModel
    from app.database.models.bit_schema.user_extension import UserExtensionModel
    from app.database.models.bit_schema.personal_background import (
        PersonalBackgroundModel,
    )
    from app.database.models.bit_schema.mentorship_relation_extension import (
        MentorshipRelationExtensionModel,
    )

    # uncomment the line below if no dummy data needed on INITIAL setup!
    # Warning !!! Do not uncomment if this is not your INITIAL setup to database!
    # db.create_all()

    # uncomment lines below if you want to add dummy data on INITIAL setup!
    # !!! Warning!!! Treat this with caution as it will mess up your db!!
    # Warning !!! Do not uncomment if this is not your INITIAL setup to elephant postgresql database!

    # from app.database.db_add_mock import add_mock_data # uncomment here
    # add_mock_data()

    @application.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "UserModel": UserModel,
            "MentorshipRelationModel": MentorshipRelationModel,
            "TaskListModel": TasksListModel,
            "TaskCommentModel": TaskCommentModel,
            "OrganizationModel": OrganizationModel,
            "ProgramModel": ProgramModel,
            "UserExtensionModel": UserExtensionModel,
            "PersonalBackgroundModel": PersonalBackgroundModel,
            "MentorshipRelationExtensionModel": MentorshipRelationExtensionModel,
        }

    # uncomment the lines below if you want to test querying database


if __name__ == "__main__":
    application.run(port=5000)
