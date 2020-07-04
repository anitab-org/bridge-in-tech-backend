from flask_restx import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[register_user_api_model.name] = register_user_api_model
    api_namespace.models[login_request_body_model.name] = login_request_body_model
    api_namespace.models[login_response_body_model.name] = login_response_body_model
    
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

login_request_body_model = Model(
    "Login request data model",
    {
        "username": fields.String(required=True, description="User's username"),
        "password": fields.String(required=True, description="User's password"),
    },
)

login_response_body_model = Model(
    "Login response data model",
    {
        "access_token": fields.String(required=True, description="User's access token"),
        "access_expiry": fields.Float(
            required=True, description="Access token expiry UNIX timestamp"
        ),
    },
)

