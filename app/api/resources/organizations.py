import ast
from http import HTTPStatus, cookies
from flask import request
from flask_restx import Resource, marshal, Namespace
from app import messages
from app.api.request_api_utils import (
    post_request, 
    get_request,
    put_request, 
    http_response_checker, 
    AUTH_COOKIE, 
    validate_token)
from app.api.resources.common import auth_header_parser
from app.api.dao.organization import OrganizationDAO
from app.api.dao.program import ProgramDAO
from app.utils.validation_utils import expected_fields_validator
from app.api.models.organization import *
from app.api.validations.organization import validate_update_organization, validate_update_program
from app.utils.bit_constants import DEFAULT_PAGE, DEFAULT_ORGANIZATIONS_PER_PAGE, DEFAULT_PROGRAMS_PER_PAGE


organizations_ns = Namespace("Organizations", description="Operations related to organizations")
add_models_to_namespace(organizations_ns)

OrganizationDAO = OrganizationDAO()
ProgramDAO = ProgramDAO()


@organizations_ns.response(
        HTTPStatus.UNAUTHORIZED.value,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
)
@organizations_ns.response(HTTPStatus.FORBIDDEN.value, f"{messages.NOT_ORGANIZATION_REPRESENTATIVE}")
@organizations_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"{messages.INTERNAL_SERVER_ERROR}")
@organizations_ns.route("organization")
class Organization(Resource):
    @classmethod
    @organizations_ns.doc("get_organization")
    @organizations_ns.response(HTTPStatus.OK.value, "Successful request", get_organization_response_model)
    @organizations_ns.response(HTTPStatus.NOT_FOUND.value, f"{messages.ORGANIZATION_DOES_NOT_EXIST}")
    @organizations_ns.expect(auth_header_parser, validate=True)
    def get(cls):
        """
        Returns organization where the current user is the representative.

        A user with valid access token can use this endpoint to view the organization
        that they represent. The endpoint doesn't take any other input. 
        """
        token = request.headers.environ["HTTP_AUTHORIZATION"]

        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            try:
                user_json = (AUTH_COOKIE["user"].value)
                user = ast.literal_eval(user_json)
                representative_name = user["name"]
                return OrganizationDAO.get_organization(int(user["id"]), representative_name)
            except ValueError as e:
                return e, HTTPStatus.BAD_REQUEST
        return is_wrong_token

    
    @classmethod
    @organizations_ns.doc("update_organization")
    @organizations_ns.response(HTTPStatus.OK.value, f"{messages.ORGANIZATION_SUCCESSFULLY_UPDATED}")
    @organizations_ns.response(HTTPStatus.CREATED.value, f"{messages.ORGANIZATION_SUCCESSFULLY_CREATED}")
    @organizations_ns.response(
        HTTPStatus.BAD_REQUEST.value,
        f"{messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT}\n"
        f"{messages.EMAIL_INPUT_BY_USER_IS_INVALID}\n"
        f"{messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT}\n"
        f"{messages.TIMEZONE_INPUT_IS_INVALID}\n"
        f"{messages.TIMEZONE_FIELD_IS_MISSING}\n"
        f"{messages.ORGANIZATION_STATUS_INPUT_IS_INVALID}\n"
        f"{messages.ORGANIZATION_OR_PROGRAM_STATUS_FIELD_IS_MISSING}\n"
        f"{messages.UNEXPECTED_INPUT}"
    )
    @organizations_ns.expect(auth_header_parser, update_organization_request_model, validate=True)
    def put(cls):
        """
        Creates or updates organization where the current user is the representative.

        A user with valid access token can use this endpoint to create or update the organization
        that they represent. The endpoint takes any of the given parameters (representative_department, 
        organization name, email, about, address, website, timezone (with value as per 
        Timezone Enum Value), phone, status (with value as per OrganizationStatus Enum Value) and join date). 
        The response contains a success or error message. 
        """
        token = request.headers.environ["HTTP_AUTHORIZATION"]

        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            data = request.json
            if not data:
                return messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT, HTTPStatus.BAD_REQUEST

            is_field_valid = expected_fields_validator(data, update_organization_request_model)
            if not is_field_valid.get("is_field_valid"):
                return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST
            
            is_not_valid = validate_update_organization(data)
            if is_not_valid:
                return is_not_valid, HTTPStatus.BAD_REQUEST

            return OrganizationDAO.update_organization(data)
              
        return is_wrong_token

    
@organizations_ns.route("organizations")
class OrganizationsList(Resource):
    @classmethod
    @organizations_ns.doc(
        "list_organizations", 
        params={
            "name": "Search by organization name", 
            "page": "Specify page of organizations", 
            "per_page": "Specify number of organizations per page"})
    @organizations_ns.response(HTTPStatus.OK.value, "Successful request", get_organization_response_model)
    @organizations_ns.response( 
        HTTPStatus.UNAUTHORIZED.value,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
    )
    @organizations_ns.response(HTTPStatus.NOT_FOUND.value, f"{messages.ORGANIZATION_DOES_NOT_EXIST}")
    @organizations_ns.response(
        HTTPStatus.INTERNAL_SERVER_ERROR.value, f"{messages.INTERNAL_SERVER_ERROR}"
    )
    @organizations_ns.expect(auth_header_parser, validate=True)
    def get(cls):
        """
        Returns list of all organizations whose names contain the given query.

        A user with valid access token can view the list of organizations. The endpoint
        doesn't take any other input. A JSON array having an object for each organization is
        returned. The array contains the organization id, representative id, representative name, 
        representative department, organization name, email, about, 
        address, website, timezone (with value as per Timezone Enum Value), phone, status 
        (with value as per OrganizationStatus Enum Value) and join date.
        """

        token = request.headers.environ["HTTP_AUTHORIZATION"]
        page = request.args.get("page", default=DEFAULT_PAGE, type=int)
        per_page = request.args.get("per_page", default=DEFAULT_ORGANIZATIONS_PER_PAGE, type=int)

        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            return OrganizationDAO.list_organizations(request.args.get("name", ""), page, per_page, token)
        return is_wrong_token


@organizations_ns.route("organizations/<int:organization_id>/programs")
class ProgramsList(Resource):
    @classmethod
    @organizations_ns.doc("list_programs")
    @organizations_ns.response(HTTPStatus.OK.value, "Successful request", get_program_response_model)
    @organizations_ns.response(
        HTTPStatus.UNAUTHORIZED.value,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
    )
    @organizations_ns.response(HTTPStatus.NOT_FOUND.value, 
        f"{messages.NO_PROGRAM_FOUND}\n"
        f"{messages.NO_ORGANIZATION_FOUND}"
    )
    @organizations_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"{messages.INTERNAL_SERVER_ERROR}")
    @organizations_ns.expect(auth_header_parser, validate=True)
    def get(cls, organization_id):
        """
        Returns list of all programs where organization ID is passed as parameter.

        A user with valid access token can view the list of programs. The endpoint
        doesn't take any other input. A JSON array having an object for each program is
        returned. The array contains the program id, program name, organization id, organization name, 
        representative id, representative name, start date, end date, description, target skills,
        target candidate, payment currency code, payment amount, contact type, zone (with value
        as per Zone Enum value), mentee's responsibility, mentor's responsibility, organization's
        responsibility, mentee's requirements, mentor's requirements, resources_provided, contact
        person's name, contact person's department, program address, contact person's phone, contact
        person's mobile, contact person's email, program webiste, irc channel, tags, status
        (with value as per ProgramStatus Enum value), and creation date.
        """

        token = request.headers.environ["HTTP_AUTHORIZATION"]
        
        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            return ProgramDAO.get_all_programs_by_organization(organization_id, token)
        return is_wrong_token


@organizations_ns.route("organizations/<int:organization_id>/programs/program")
class CreateProgram(Resource):
    @classmethod
    @organizations_ns.doc("create_program")
    @organizations_ns.response(HTTPStatus.CREATED.value, f"{messages.PROGRAM_SUCCESSFULLY_CREATED}")
    @organizations_ns.response(
        HTTPStatus.BAD_REQUEST.value,
        f"{messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT}\n"
        f"{messages.EMAIL_INPUT_BY_USER_IS_INVALID}\n"
        f"{messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT}\n"
        f"{messages.TIMEZONE_INPUT_IS_INVALID}\n"
        f"{messages.TIMEZONE_FIELD_IS_MISSING}\n"
        f"{messages.ORGANIZATION_STATUS_INPUT_IS_INVALID}\n"
        f"{messages.ORGANIZATION_OR_PROGRAM_STATUS_FIELD_IS_MISSING}\n"
        f"{messages.UNEXPECTED_INPUT}"
    )
    @organizations_ns.response(
        HTTPStatus.UNAUTHORIZED.value,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
    )
    @organizations_ns.response(
        HTTPStatus.FORBIDDEN.value, 
        f"{messages.NOT_ORGANIZATION_REPRESENTATIVE}\n"
        f"{messages.USER_IS_NOT_THE_ORGANIZATION_REPRESENTATIVE}"
    )
    @organizations_ns.response(HTTPStatus.NOT_FOUND.value, f"{messages.ORGANIZATION_DOES_NOT_EXIST}") 
    @organizations_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"{messages.INTERNAL_SERVER_ERROR}")
    @organizations_ns.expect(auth_header_parser, update_program_request_model, validate=True)
    def post(cls, organization_id):
        """
        Creates a program where organization id is passed.

        A user with valid access token can use this endpoint to create a program.
        The endpoint takes any of the given parameters (program name, start date, 
        end date, description, target skills, target candidate selected from any of
        the gender (value as per Gender enum), age (Age enum), ethnicity (Ethnicity enum), 
        sexual orientation (SexualOrientation enum), religion (Religion enum), physical 
        ability (PhysicalAbility enum), mental ability (MentalAbility enum), socio economic
        (SocioEEconomic enum), highest education (HighestEducation enum), years of experience
        (YearsOfExperience enum), or other which value is self-defined by organization, payment 
        currency code, payment amount, contact type (value as per ContactType enum), zone 
        (with value as per Zone Enum value), mentee's responsibility, mentor's responsibility, 
        organization's responsibility, mentee's requirements, mentor's requirements, 
        resources provided, contact person's name, contact person's department, program address, 
        contact person's phone, contact person's mobile, contact person's email, program webiste, 
        irc channel, tags, status (with value as per ProgramStatus Enum value), and creation date.
        """
        token = request.headers.environ["HTTP_AUTHORIZATION"]

        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            data = request.json
            if not data:
                return messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT, HTTPStatus.BAD_REQUEST

            is_field_valid = expected_fields_validator(data, update_program_request_model)
            if not is_field_valid.get("is_field_valid"):
                return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST
            
            is_not_valid = validate_update_program(data)
            if is_not_valid:
                return is_not_valid, HTTPStatus.BAD_REQUEST

            return ProgramDAO.create_program(organization_id, data)
        return is_wrong_token


@organizations_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, f"{messages.INTERNAL_SERVER_ERROR}")
@organizations_ns.response(
    HTTPStatus.NOT_FOUND.value, 
    f"{messages.NO_PROGRAM_FOUND}\n"
    f"{messages.ORGANIZATION_DOES_NOT_EXIST}\n"
    f"{messages.PROGRAM_DOES_NOT_EXIST}"
)
@organizations_ns.response(
    HTTPStatus.UNAUTHORIZED.value,
    f"{messages.TOKEN_HAS_EXPIRED}\n"
    f"{messages.TOKEN_IS_INVALID}\n"
    f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
)
@organizations_ns.param("organization_id", "The organization identifier")
@organizations_ns.param("program_id", "The program identifier")
@organizations_ns.route("organizations/<int:organization_id>/programs/<int:program_id>")
class Program(Resource):
    @classmethod
    @organizations_ns.doc("get_program")
    @organizations_ns.response(HTTPStatus.OK.value, "Successful request", get_program_response_model)
    @organizations_ns.expect(auth_header_parser, validate=True)
    def get(cls, organization_id, program_id):
        """
        Returns a program which program ID and organization ID are passed as parameters.

        A user with valid access token can view the program within specific organization 
        which IDs are passed as parameters.The endpoint doesn't take any other input. 
        An program object is returned which contains the program id, program name, organization 
        id, organization name, representative id, representative name, start date, end date, 
        description, target skills, target candidate, payment currency code, payment amount, 
        contact type, zone (with value as per Zone Enum value), mentee's responsibility, 
        mentor's responsibility, organization's responsibility, mentee's requirements, mentor's 
        requirements, resources_provided, contact person's name, contact person's department, 
        program address, contact person's phone, contact person's mobile, contact person's 
        email, program webiste, irc channel, tags, status (with value as per ProgramStatus Enum 
        value), and creation date.
        """
        
        token = request.headers.environ["HTTP_AUTHORIZATION"]
        
        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            return ProgramDAO.get_program_by_program_id(organization_id, program_id, token)
        return is_wrong_token


    @classmethod
    @organizations_ns.doc("update_program")
    @organizations_ns.response(HTTPStatus.OK.value, f"{messages.PROGRAM_SUCCESSFULLY_UPDATED}")
    @organizations_ns.response(
        HTTPStatus.BAD_REQUEST.value,
        f"{messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT}\n"
        f"{messages.EMAIL_INPUT_BY_USER_IS_INVALID}\n"
        f"{messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT}\n"
        f"{messages.PROGRAM_STATUS_INPUT_IS_INVALID}\n"
        f"{messages.ORGANIZATION_OR_PROGRAM_STATUS_FIELD_IS_MISSING}\n"
        f"{messages.UNEXPECTED_INPUT}"
    )
    @organizations_ns.expect(auth_header_parser, update_program_request_model, validate=True)
    def put(cls, organization_id, program_id):
        """
        Updates a program where program ID and organization id are passed as parameters.

        A user with valid access token can use this endpoint to update a program.
        The endpoint takes any of the given parameters (program name, start date, 
        end date, description, target skills, target candidate selected from any of
        the gender (value as per Gender enum), age (Age enum), ethnicity (Ethnicity enum), 
        sexual orientation (SexualOrientation enum), religion (Religion enum), physical 
        ability (PhysicalAbility enum), mental ability (MentalAbility enum), socio economic
        (SocioEEconomic enum), highest education (HighestEducation enum), years of experience
        (YearsOfExperience enum), or other which value is self-defined by organization, payment 
        currency code, payment amount, contact type (value as per ContactType enum), zone 
        (with value as per Zone Enum value), mentee's responsibility, mentor's responsibility, 
        organization's responsibility, mentee's requirements, mentor's requirements, 
        resources provided, contact person's name, contact person's department, program address, 
        contact person's phone, contact person's mobile, contact person's email, program webiste, 
        irc channel, tags, status (with value as per ProgramStatus Enum value), and creation date.
        """
        token = request.headers.environ["HTTP_AUTHORIZATION"]

        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            data = request.json
            if not data:
                return messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT, HTTPStatus.BAD_REQUEST

            is_field_valid = expected_fields_validator(data, update_program_request_model)
            if not is_field_valid.get("is_field_valid"):
                return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST
            
            is_not_valid = validate_update_program(data)
            if is_not_valid:
                return is_not_valid, HTTPStatus.BAD_REQUEST

            return ProgramDAO.update_program(organization_id, program_id, data)
        return is_wrong_token

