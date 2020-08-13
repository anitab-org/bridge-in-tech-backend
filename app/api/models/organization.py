from flask_restx import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[update_organization_request_model.name] = update_organization_request_model
    api_namespace.models[get_organization_response_model.name] = get_organization_response_model

update_organization_request_model = Model(
    "Creates or updates organization request model",
    {
        "representative_department": fields.String(required=True, description="Representative department"),
        "name": fields.String(required=True, description="Organization's name"),
        "email": fields.String(required=True, description="Organization's email"),
        "about": fields.String(required=False, description="About the organization"),
        "address": fields.String(required=False, description="Organization's address"),
        "website": fields.String(required=True, description="Organization's website"),
        "timezone": fields.String(required=True, description="Organization's timezone"),
        "phone": fields.String(required=True, description="Organization's phone"),
        "status": fields.String(required=True, description="Organization's profile status"),
    },
)

get_organization_response_model = Model(
    "Retrieves organization response model",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of an organization"
        ),
        "representative_id": fields.Integer(required=True, description="Representative id"),
        "representative_name": fields.String(required=True, description="Representative name"),
        "representative_department": fields.String(required=True, description="Representative department"),
        "organization_name": fields.String(required=True, description="Organization's name"),
        "email": fields.String(required=True, description="Organization's email"),
        "about": fields.String(required=False, description="About the organization"),
        "address": fields.String(required=False, description="Organization's address"),
        "website": fields.String(required=True, description="Organization's website"),
        "timezone": fields.String(required=True, description="Organization's timezone"),
        "phone": fields.String(required=True, description="Organization's phone"),
        "status": fields.String(required=True, description="Organization's profile status"),
        "join_date": fields.Float(required=True, description="Organization's join date"),
    },
)