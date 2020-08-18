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
from app.utils.validation_utils import expected_fields_validator
from app.api.models.organization import *
from app.api.validations.organization import validate_update_organization
from app.utils.bit_constants import DEFAULT_PAGE, DEFAULT_ORGANIZATIONS_PER_PAGE


organizations_ns = Namespace("Organizations", description="Operations related to organizations")
add_models_to_namespace(organizations_ns)

OrganizationDAO = OrganizationDAO()


@organizations_ns.response(
        HTTPStatus.UNAUTHORIZED,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
)
@organizations_ns.response(HTTPStatus.FORBIDDEN, f"{messages.NOT_ORGANIZATION_REPRESENTATIVE}")
@organizations_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}")
@organizations_ns.route("organization")
class Organization(Resource):
    @classmethod
    @organizations_ns.doc("get_organization")
    @organizations_ns.response(HTTPStatus.NOT_FOUND, f"{messages.ORGANIZATION_DOES_NOT_EXIST}")
    @organizations_ns.response(HTTPStatus.OK, "Successful request", get_organization_response_model)
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
    @organizations_ns.response(HTTPStatus.OK, "Successful request", update_organization_request_model)
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
        @organizations_ns.doc("list_organizations", params={"name": "Search by organization name", "page": "Specify page of organizations", "per_page": "Specify number of organizations per page"})
        @organizations_ns.response(
            HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}"
        )
        @organizations_ns.response(HTTPStatus.NOT_FOUND, f"{messages.ORGANIZATION_DOES_NOT_EXIST}")
        @organizations_ns.response( 
        HTTPStatus.UNAUTHORIZED,
            f"{messages.TOKEN_HAS_EXPIRED}\n"
            f"{messages.TOKEN_IS_INVALID}\n"
            f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
        )
        @organizations_ns.response(HTTPStatus.OK, "Successful request", get_organization_response_model)
        @organizations_ns.expect(auth_header_parser, validate=True)
        def get(cls):
            """
            Returns list of all organizations whose names contain the given query.

            A user with valid access token can view the list of organizations. The endpoint
            doesn't take any other input. A JSON array having an object for each organization is
            returned. The array contains the representative id, rep_department, organization name, email, about, 
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


        


