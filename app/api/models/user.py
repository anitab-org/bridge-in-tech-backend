from flask_restx import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[register_user_api_model.name] = register_user_api_model
    api_namespace.models[login_request_body_model.name] = login_request_body_model
    api_namespace.models[login_response_body_model.name] = login_response_body_model
    api_namespace.models[full_user_api_model.name] = full_user_api_model
    api_namespace.models[update_user_details_request_body_model.name] = update_user_details_request_body_model
    api_namespace.models[get_user_extension_response_model.name] = get_user_extension_response_model
    api_namespace.models[user_extension_request_body_model.name] = user_extension_request_body_model
    api_namespace.models[get_user_personal_background_response_model.name] = get_user_personal_background_response_model
    api_namespace.models[user_personal_background_request_body_model.name] = user_personal_background_request_body_model
    api_namespace.models[public_user_personal_details_response_model.name] = public_user_personal_details_response_model

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

full_user_api_model = Model(
    "User Complete model used in listing",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of a user"
        ),
        "name": fields.String(required=True, description="User name"),
        "username": fields.String(required=True, description="User username"),
        "email": fields.String(required=True, description="User email"),
        "terms_and_conditions_checked": fields.Boolean(
            required=True, description="User Terms and Conditions check state"
        ),
        "is_admin": fields.Boolean(required=True, description="User admin status"),
        "registration_date": fields.Float(
            required=True, description="User registration date"
        ),
        "is_email_verified": fields.Boolean(
            required=True, description="User email verification status"
        ),
        "email_verification_date": fields.DateTime(
            required=False, description="User email verification date"
        ),
        "bio": fields.String(required=False, description="User bio"),
        "location": fields.String(required=False, description="User location"),
        "occupation": fields.String(required=False, description="User occupation"),
        "current_organization": fields.String(required=False, description="User current organization"),
        "slack_username": fields.String(
            required=False, description="User slack username"
        ),
        "social_media_links": fields.String(
            required=False, description="User social media links"
        ),
        "skills": fields.String(required=False, description="User skills"),
        "interests": fields.String(required=False, description="User interests"),
        "resume_url": fields.String(required=False, description="User resume url"),
        "photo_url": fields.String(required=False, description="User photo url"),
        "need_mentoring": fields.Boolean(
            required=False, description="User need mentoring indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=False, description="User availability to mentor indication"
        ),
        "current_mentorship_role": fields.Integer(
            required=False, description="User current role"
        ),
        "membership_status": fields.Integer(
            required=False, description="User membershipstatus"
        ),
    },
)

update_user_details_request_body_model = Model(
    "Update User details request data model",
    {
        "name": fields.String(required=False, description="User name"),
        "username": fields.String(required=False, description="User username"),
        "bio": fields.String(required=False, description="User bio"),
        "location": fields.String(required=False, description="User location"),
        "occupation": fields.String(required=False, description="User occupation"),
        "current_organization": fields.String(required=False, description="User current organization"),
        "slack_username": fields.String(
            required=False, description="User slack username"
        ),
        "social_media_links": fields.String(
            required=False, description="User social media links"
        ),
        "skills": fields.String(required=False, description="User skills"),
        "interests": fields.String(required=False, description="User interests"),
        # TODO: This url is generated by the MS backend
        "resume_url": fields.String(required=False, description="User resume url"),
        # TODO: This url is generated by the MS backend
        "photo_url": fields.String(required=False, description="User photo url"),
        "need_mentoring": fields.Boolean(
            required=False, description="User need mentoring indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=False, description="User availability to mentor indication"
        ),
    },
)

get_user_extension_response_model = Model(
    "Retrieve additional information response data model",
    {
        "user_id": fields.Integer(required=True, description="User Id"),
        "is_organization_rep": fields.Boolean(required=True, description="User represents organization"),
        "timezone": fields.String(required=True, description="User's timezone"),
        "phone": fields.String(required=False, description="phone"),
        "mobile": fields.String(required=False, description="mobile"),
        "personal_website": fields.String(required=False, description="personal_website"),
    }
)

user_extension_request_body_model = Model(
    "Create or Update user's additional information data model",
    {
        "is_organization_rep": fields.Boolean(required=True, description="User represents organization"),
        "timezone": fields.String(required=True, description="User's timezone"),
        "phone": fields.String(required=False, description="phone"),
        "mobile": fields.String(required=False, description="mobile"),
        "personal_website": fields.String(required=False, description="personal_website"),
    }
)

get_user_personal_background_response_model = Model(
    "Retrieve personal background infomation response data model",
    {
        "user_id": fields.Integer(required=True, description="user_id"),
        "gender": fields.String(required=True, description="gender"),
        "age": fields.String(required=True, description="age"),
        "ethnicity": fields.String(required=True, description="ethnicity"),
        "sexual_orientation": fields.String(required=True, description="sexual_orientation"),
        "religion": fields.String(required=True, description="religion"),
        "physical_ability": fields.String(required=True, description="physical_ability"),
        "mental_ability": fields.String(required=True, description="mental_ability"),
        "socio_economic": fields.String(required=True, description="socio_economic"),
        "highest_education": fields.String(required=True, description="highest_education"),
        "years_of_experience": fields.String(required=True, description="years_of_experience"),
        "others": fields.String(required=True, description="others"),
        "gender_other": fields.String(required=False, description="gender_other"),
        "ethnicity_other": fields.String(required=False, description="ethnicity_other"),
        "sexual_orientation_other": fields.String(required=False, description="sexual_orientation_other"),
        "religion_other": fields.String(required=False, description="religion_other"),
        "physical_ability_other": fields.String(required=False, description="physical_ability_other"),
        "mental_ability_other": fields.String(required=False, description="mental_ability_other"),
        "socio_economic_other": fields.String(required=False, description="socio_economic_other"),
        "highest_education_other": fields.String(required=False, description="highest_education_other"),
        "is_public": fields.Boolean(required=True, description="is_public"),
    }
)

user_personal_background_request_body_model = Model(
    "Create or update personal background information request model",
    {
        "gender": fields.String(required=True, description="gender"),
        "age": fields.String(required=True, description="age"),
        "ethnicity": fields.String(required=True, description="ethnicity"),
        "sexual_orientation": fields.String(required=True, description="sexual_orientation"),
        "religion": fields.String(required=True, description="religion"),
        "physical_ability": fields.String(required=True, description="physical_ability"),
        "mental_ability": fields.String(required=True, description="mental_ability"),
        "socio_economic": fields.String(required=True, description="socio_economic"),
        "highest_education": fields.String(required=True, description="highest_education"),
        "years_of_experience": fields.String(required=True, description="years_of_experience"),
        "gender_other": fields.String(required=False, description="gender_other"),
        "ethnicity_other": fields.String(required=False, description="ethnicity_other"),
        "sexual_orientation_other": fields.String(required=False, description="sexual_orientation_other"),
        "religion_other": fields.String(required=False, description="religion_other"),
        "physical_ability_other": fields.String(required=False, description="physical_ability_other"),
        "mental_ability_other": fields.String(required=False, description="mental_ability_other"),
        "socio_economic_other": fields.String(required=False, description="socio_economic_other"),
        "highest_education_other": fields.String(required=False, description="highest_education_other"),
        "is_public": fields.Boolean(required=True, description="is_public"),
    }
)

public_user_personal_details_response_model = Model(
    "User personal details list model",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of a user"
        ),
        "username": fields.String(required=True, description="User username"),
        "name": fields.String(required=True, description="User name"),
        "slack_username": fields.String(
            required=True, description="User Slack username"
        ),
        "bio": fields.String(required=True, description="User bio"),
        "location": fields.String(required=True, description="User location"),
        "occupation": fields.String(required=True, description="User occupation"),
        "current_organization": fields.String(required=True, description="User current_organization"),
        "interests": fields.String(required=True, description="User interests"),
        "skills": fields.String(required=True, description="User skills"),
        "need_mentoring": fields.Boolean(
            required=True, description="User need to be mentored indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=True, description="User availability to mentor indication"
        ),
        "is_available": fields.Boolean(
            required=True,
            description="User availability to mentor or to be mentored indication",
        ),
    },
)
