from flask_restx import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[update_organization_request_model.name] = update_organization_request_model
    api_namespace.models[get_organization_response_model.name] = get_organization_response_model
    api_namespace.models[update_program_request_model.name] = update_program_request_model
    api_namespace.models[get_program_response_model.name] = get_program_response_model


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

update_program_request_model = Model(
    "Creates or updates program request model",
    {
        "program_name": fields.String(required=True, description="Program name"),
        "start_date": fields.String(required=True, description="The start date of the program with format YYYY-MM-DD HH:MM"),
        "end_date": fields.String(required=True, description="The end date of the program with format YYYY-MM-DD HH:MM"),
        "description": fields.String(required=False, description="The program description"),
        "target_skills": fields.List(fields.String, required=False, description="The target skills required for the program"),
        "target_candidate_gender": fields.String(required=False, description="The target candidate for the program from gender category"),
        "target_candidate_age": fields.String(required=False, description="The target candidate for the program from age category"),
        "target_candidate_ethnicity": fields.String(required=False, description="The target candidate for the program from ethinicity category"),
        "target_candidate_sexual_orientation": fields.String(required=False, description="The target candidate for the program from sexual_orientation category"),
        "target_candidate_religion": fields.String(required=False, description="The target candidate for the program from religion category"),
        "target_candidate_physical_ability": fields.String(required=False, description="The target candidate for the program from physical_ability category"),
        "target_candidate_mental_ability": fields.String(required=False, description="The target candidate for the program from mental_ability category"),
        "target_candidate_socio_economic": fields.String(required=False, description="The target candidate for the program from socio_economic category"),
        "target_candidate_highest_education": fields.String(required=False, description="The target candidate for the program from highest_education category"),
        "target_candidate_years_of_experience": fields.String(required=False, description="The target candidate for the program from years_of_experience category"),
        "target_candidate_other": fields.String(required=False, description="The target candidate for the program from organization classification"),
        "payment_currency": fields.String(required=False, description="The currency code"),
        "payment_amount": fields.Integer(required=False, description="The currency amount"),
        "contact_type": fields.String(required=False, description="The type of contact between participants of the program"),
        "zone": fields.String(required=False, description="The scope of the program in respect to its location"),
        "student_responsibility": fields.List(fields.String, required=False, description="The responsibility of the mentee in the program"),
        "mentor_responsibility": fields.List(fields.String, required=False, description="The responsibility of the mentor in the program"),
        "organization_responsibility": fields.List(fields.String, required=False, description="The responsibility of the organization in the program"),
        "student_requirements": fields.List(fields.String, required=False, description="The requirement of a mentee for the program"),
        "mentor_requirements": fields.List(fields.String, required=False, description="The requirement of a mentor for the program"),
        "resources_provided": fields.List(fields.String, required=False, description="The resources provided by the organization for the program"),
        "contact_name": fields.String(required=False, description="The program contact person's name"),
        "contact_department": fields.String(required=False, description="The program contact person's department"),
        "program_address": fields.String(required=False, description="The address where the program is held"),
        "contact_phone": fields.String(required=False, description="The program contact person's phone number"),
        "contact_mobile": fields.String(required=False, description="The program contact person's mobile number"),
        "contact_email": fields.String(required=False, description="The program contact person's email address"),
        "program_website": fields.String(required=False, description="The program website link"),
        "irc_channel": fields.String(required=False, description="The program IRC channel link"),
        "tags": fields.List(fields.String, required=False, description="The program tags which can be based on skills or type of candidates"),
        "status": fields.String(required=False, description="The program current status"),
    },
)

get_program_response_model = Model(
    "Retrieves program response model",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of a program",
        ),
        "program_name": fields.String(required=True, description="Program name"),
        "organization_id": fields.Integer(
            readOnly=True, description="The unique identifier of an organization",
        ),
        "organization_name": fields.String(
            required=True, description="The organization name where the program is offered"),
        "representative_id": fields.Integer(
            readOnly=True, description="The unique identifier of the user representative",
        ),
        "representative_name": fields.String(required=True, description="The organization representative name"),
        "start_date": fields.String(required=True, description="The start date of the program"),
        "end_date": fields.String(required=True, description="The end date of the program"),
        "description": fields.String(required=False, description="The program description"),
        "target_skills": fields.List(fields.String, required=False, description="The target skills required for the program"),
        "target_candidate_gender": fields.String(required=False, description="The target candidate for the program from gender category"),
        "target_candidate_age": fields.String(required=False, description="The target candidate for the program from age category"),
        "target_candidate_ethnicity": fields.String(required=False, description="The target candidate for the program from ethinicity category"),
        "target_candidate_sexual_orientation": fields.String(required=False, description="The target candidate for the program from sexual_orientation category"),
        "target_candidate_religion": fields.String(required=False, description="The target candidate for the program from religion category"),
        "target_candidate_physical_ability": fields.String(required=False, description="The target candidate for the program from physical_ability category"),
        "target_candidate_mental_ability": fields.String(required=False, description="The target candidate for the program from mental_ability category"),
        "target_candidate_socio_economic": fields.String(required=False, description="The target candidate for the program from socio_economic category"),
        "target_candidate_highest_education": fields.String(required=False, description="The target candidate for the program from highest_education category"),
        "target_candidate_years_of_experience": fields.String(required=False, description="The target candidate for the program from years_of_experience category"),
        "target_candidate_other": fields.String(required=False, description="The target candidate for the program from organization classification"),
        "payment_currency": fields.String(required=False, description="The currency code"),
        "payment_amount": fields.Integer(required=False, description="The currency amount"),
        "contact_type": fields.String(required=False, description="The type of contact between participants of the program"),
        "zone": fields.String(required=False, description="The scope of the program in respect to its location"),
        "student_responsibility": fields.List(fields.String, required=False, description="The responsibility of the mentee in the program"),
        "mentor_responsibility": fields.List(fields.String, required=False, description="The responsibility of the mentor in the program"),
        "organization_responsibility": fields.List(fields.String, required=False, description="The responsibility of the organization in the program"),
        "student_requirements": fields.List(fields.String, required=False, description="The requirement of a mentee for the program"),
        "mentor_requirements": fields.List(fields.String, required=False, description="The requirement of a mentor for the program"),
        "resources_provided": fields.List(fields.String, required=False, description="The resources provided by the organization for the program"),
        "contact_name": fields.String(required=False, description="The program contact person's name"),
        "contact_department": fields.String(required=False, description="The program contact person's department"),
        "program_address": fields.String(required=False, description="The address where the program is held"),
        "contact_phone": fields.String(required=False, description="The program contact person's phone number"),
        "contact_mobile": fields.String(required=False, description="The program contact person's mobile number"),
        "contact_email": fields.String(required=False, description="The program contact person's email address"),
        "program_website": fields.String(required=False, description="The program website link"),
        "irc_channel": fields.String(required=False, description="The program IRC channel link"),
        "tags": fields.List(fields.String, required=False, description="The program tags which can be based on skills or type of candidates"),
        "status": fields.String(required=False, description="The program current status"),
        "creation_date": fields.String(required=False, description="The creation date of the program"),
    }
)
