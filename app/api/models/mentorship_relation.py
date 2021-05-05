from flask_restx import fields, Model

from app.utils.enum_utils import MentorshipRelationState


def add_models_to_namespace(api_namespace):
    api_namespace.models[send_mentorship_extension_request_body.name] = send_mentorship_extension_request_body


send_mentorship_extension_request_body = Model(
    "Send mentorship relation request to organziation model",
    {
        "mentee_id": fields.Integer(
            required=True, description="Mentorship relation mentee ID"
        ),        
        "mentee_request_date": fields.Float(
            required=True, description="Mentorship relation mentee_request_date in UNIX timestamp format"
        ),
        "end_date": fields.Float(
            required=True,
            description="Mentorship relation end date in UNIX timestamp format",
        ),
        "notes": fields.String(required=True, description="Mentorship relation notes"), 
    
    },
)
