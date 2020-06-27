from flask_restx import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[register_user_api_model.name] = register_user_api_model

register_user_api_model = Model(
    "User registration model",
    {
        "name": fields.String(required=True, description="User name"),
        "username": fields.String(required=True, description="User username"),
        "password": fields.String(required=True, description="User password"),
        "email": fields.String(required=True, description="User email"),
        "terms_and_conditions_checked": fields.Boolean(
            required=True, description="User check Terms and Conditions value"
        ),
        "need_mentoring": fields.Boolean(
            required=False, description="User need mentoring indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=False, description="User availability to mentor indication"
        ),
    },
)
