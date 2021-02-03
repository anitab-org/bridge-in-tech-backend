import ast
import json
from http import HTTPStatus, cookies
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, marshal, Namespace
from app import messages
from app.api.request_api_utils import (
    post_request, 
    post_request_with_token,
    get_request,
    put_request, 
    http_response_checker, 
    AUTH_COOKIE, 
    validate_token)
# Common Resources
from app.api.resources.common import auth_header_parser
# Validations
from app.api.validations.user import *
from app.api.validations.task_comment import (
    validate_task_comment_request_data,
    COMMENT_MAX_LENGTH,
)
from app.utils.validation_utils import get_length_validation_error_message,expected_fields_validator
from app.utils.ms_constants import DEFAULT_PAGE, DEFAULT_USERS_PER_PAGE
# Namespace Models
from app.api.models.mentorship_relation import *
# Databases Models
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.ms_schema.mentorship_relation import MentorshipRelationModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.program import ProgramModel
# DAOs
from app.api.dao.user_extension import UserExtensionDAO
from app.api.dao.personal_background import PersonalBackgroundDAO
from app.api.dao.mentorship_relation_extension import MentorshipRelationExtensionDAO
from app.api.dao.organization import OrganizationDAO
from app.api.dao.program import ProgramDAO

mentorship_relation_ns = Namespace(
    "Mentorship Relation",
    description="Operations related to " "mentorship relations " "between users",
)
add_models_to_namespace(mentorship_relation_ns)

mentorshipRelationExtensionDAO = MentorshipRelationExtensionDAO()
userExtensionDAO = UserExtensionDAO()
OrganizationDAO = OrganizationDAO()
ProgramDAO = ProgramDAO()

@mentorship_relation_ns.route("organizations/<int:organization_id>/programs/<int:program_id>/send_request")
class SendRequest(Resource):
    @classmethod
    @mentorship_relation_ns.doc("send_request")
    @mentorship_relation_ns.expect(auth_header_parser, send_mentorship_extension_request_body)
    @mentorship_relation_ns.response(
        HTTPStatus.CREATED, "%s" % messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY
    )
    @mentorship_relation_ns.response(
        HTTPStatus.BAD_REQUEST,
        "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s"
        % (
            messages.NO_DATA_WAS_SENT,
            messages.MATCH_EITHER_MENTOR_OR_MENTEE,
            messages.MENTOR_ID_SAME_AS_MENTEE_ID,
            messages.END_TIME_BEFORE_PRESENT,
            messages.MENTOR_TIME_GREATER_THAN_MAX_TIME,
            messages.MENTOR_TIME_LESS_THAN_MIN_TIME,
            messages.MENTOR_NOT_AVAILABLE_TO_MENTOR,
            messages.MENTEE_NOT_AVAIL_TO_BE_MENTORED,
            messages.MENTOR_ALREADY_IN_A_RELATION,
            messages.MENTEE_ALREADY_IN_A_RELATION,
            messages.MENTOR_ID_FIELD_IS_MISSING,
            messages.MENTEE_ID_FIELD_IS_MISSING,
            messages.NOTES_FIELD_IS_MISSING,
            messages.ORGANIZATION_DOES_NOT_EXIST,
            messages.PROGRAM_DOES_NOT_EXIST,
        ),
    )
    @mentorship_relation_ns.response(
        HTTPStatus.UNAUTHORIZED,
        "%s\n%s\n%s"
        % (
            messages.TOKEN_HAS_EXPIRED,
            messages.TOKEN_IS_INVALID,
            messages.AUTHORISATION_TOKEN_IS_MISSING,
        ),
    )
    @mentorship_relation_ns.response(
        HTTPStatus.NOT_FOUND,
        "%s\n%s" % (messages.MENTOR_DOES_NOT_EXIST, messages.MENTEE_DOES_NOT_EXIST),
    )
    def post(cls,organization_id,program_id):
        """
        Creates a new mentorship relation request.

        Also, sends an email notification to the recipient about new relation request.

        Input:
        1. Header: valid access token
        2. Body: A dict containing
        - mentor_request_date,end_date: UNIX timestamp
        - notes: description of relation request

        Returns:
        Success or failure message. A mentorship request is send to the other
        person whose ID is mentioned. The relation appears at /pending endpoint.
        """

        token = request.headers.environ["HTTP_AUTHORIZATION"]
        is_wrong_token = validate_token(token)
            
        if not is_wrong_token:
            try:
                user_json = (AUTH_COOKIE["user"].value)
                user = ast.literal_eval(user_json)
                data = request.json
                
                if not data:
                    return messages.NO_DATA_WAS_SENT, HTTPStatus.BAD_REQUEST
        
                is_field_valid = expected_fields_validator(data, send_mentorship_extension_request_body)
                if not is_field_valid.get("is_field_valid"):
                    return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST

                is_valid = SendRequest.is_valid_data(data)
                if is_valid != {}:
                    return is_valid, HTTPStatus.BAD_REQUEST
                
                # Checking whether organization exists
                organization = OrganizationModel.query.filter_by(id=organization_id).first() 
                if not organization:
                    return messages.ORGANIZATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND 
                
                # Checking whether program exists
                program = ProgramModel.find_by_id(program_id)
                if not program or (program.organization_id != organization_id):
                    return messages.PROGRAM_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
                 
                mentor_id = organization.rep_id
                mentee_id = data['mentee_id']
                
                mentorship_relation_data={}
                mentorship_relation_data['mentee_id'] = mentee_id
                mentorship_relation_data['mentor_id'] = int(mentor_id)
                mentorship_relation_data['end_date'] = data['end_date']
                mentorship_relation_data['notes'] = data['notes']

                response = http_response_checker(post_request_with_token("/mentorship_relation/send_request",token, mentorship_relation_data))
                if response.status_code == 201:
                    mentorshipRelationId = MentorshipRelationModel.query.filter_by(mentor_id=mentor_id).filter_by(mentee_id=mentee_id).first().id
                    return MentorshipRelationExtensionDAO.createMentorshipRelationExtension(program_id, mentorshipRelationId ,data['mentee_request_date'])
                else:
                    return response.message, HTTPStatus.BAD_REQUEST
            except ValueError as e:
                return e, HTTPStatus.BAD_REQUEST
        
        return is_wrong_token
        

    @staticmethod
    def is_valid_data(data):

        # Verify if request body has required fields
        if "mentee_id" not in data:
            return messages.MENTEE_ID_FIELD_IS_MISSING
        if "end_date" not in data:
            return messages.END_DATE_FIELD_IS_MISSING
        if "notes" not in data:
            return messages.NOTES_FIELD_IS_MISSING
        if "mentee_request_date" not in data:
            return messages.MENTEE_REQUEST_DATE_FIELD_IS_MISSING
        return {}
