import json
from http import HTTPStatus, cookies
from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_restx import Resource, marshal, Namespace
from app import messages
from app.api.request_api_utils import (
    post_request, 
    get_request, 
    put_request, 
    http_response_checker, 
    AUTH_COOKIE, 
    validate_token)
from app.api.validations.user import *
from app.api.resources.common import auth_header_parser
from app.api.models.user import *
from app.api.dao.user_extension import UserExtensionDAO
from app.utils.validation_utils import expected_fields_validator
from app.database.models.bit_schema.user_extension import UserExtensionModel

users_ns = Namespace("Users", description="Operations related to users")
add_models_to_namespace(users_ns)

UserExtensionDAO = UserExtensionDAO()

@users_ns.route("register")
class UserRegister(Resource):
    @classmethod
    @users_ns.doc("create_user")
    @users_ns.doc(
        responses={
            HTTPStatus.INTERNAL_SERVER_ERROR: f"{messages.INTERNAL_SERVER_ERROR['message']}"
        }
    )
    @users_ns.response(
        HTTPStatus.CREATED, f"{messages.USER_WAS_CREATED_SUCCESSFULLY}"
    )
    @users_ns.response(
        HTTPStatus.BAD_REQUEST,
        f"{messages.NAME_INPUT_BY_USER_IS_INVALID}\n"
        f"{messages.USERNAME_INPUT_BY_USER_IS_INVALID}\n"
        f"{messages.EMAIL_INPUT_BY_USER_IS_INVALID}\n"
        f"{messages.PASSWORD_INPUT_BY_USER_HAS_INVALID_LENGTH}\n"
        f"{messages.TERMS_AND_CONDITIONS_ARE_NOT_CHECKED}\n"
        f"{messages.UNEXPECTED_INPUT}"
    )
    @users_ns.response(
        HTTPStatus.CONFLICT,
        f"{messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS}\n"
        f"{messages.USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS}"
    )
    @users_ns.response(
        HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}"
    )
    @users_ns.expect(register_user_api_model, validate=True)
    def post(cls):
        """
        Creates a new user.

        The endpoint accepts user input related to Mentorship System API (name, username, password, email,
        terms_and_conditions_checked(true/false), need_mentoring(true/false),
        available_to_mentor(true/false)).
        A success message is displayed and verification email is sent to the user's email ID.
        """

        data = request.json

        is_field_valid = expected_fields_validator(data, register_user_api_model)
        if not is_field_valid.get("is_field_valid"):
            return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST

        is_not_valid = validate_user_registration_request_data(data)
        if is_not_valid:
            return is_not_valid, HTTPStatus.BAD_REQUEST
            
        return http_response_checker(post_request("/register", data))

        
@users_ns.route("login")
class LoginUser(Resource):
    @classmethod
    @users_ns.doc("login")
    @users_ns.response(HTTPStatus.OK, "Successful login", login_response_body_model)
    @users_ns.response(
        HTTPStatus.BAD_REQUEST,
        f"{messages.USERNAME_FIELD_IS_MISSING}\n" 
        f"{messages.PASSWORD_FIELD_IS_MISSING}"
    )
    @users_ns.response(HTTPStatus.UNAUTHORIZED, f"{messages.WRONG_USERNAME_OR_PASSWORD}")
    @users_ns.response(HTTPStatus.FORBIDDEN, f"{messages.USER_HAS_NOT_VERIFIED_EMAIL_BEFORE_LOGIN}")
    @users_ns.response(
        HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}"
    )
    @users_ns.expect(login_request_body_model)
    def post(cls):
        """
        Login user

        The user can login with (username or email) + password.
        Username field can be either the User's username or the email.
        The return value is an access token and the expiry timestamp.
        The token is valid for 1 week.
        """
        data = request.json
        
        username = data.get("username", None)
        password = data.get("password", None)

        is_field_valid = expected_fields_validator(data, login_request_body_model)
        if not is_field_valid.get("is_field_valid"):
            return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST

        if not username:
            return messages.USERNAME_FIELD_IS_MISSING, HTTPStatus.BAD_REQUEST
        if not password:
            return messages.PASSWORD_FIELD_IS_MISSING, HTTPStatus.BAD_REQUEST

        return http_response_checker(post_request("/login", data))
        
@users_ns.response(
        HTTPStatus.UNAUTHORIZED,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
)
@users_ns.response(HTTPStatus.NOT_FOUND, f"{messages.USER_DOES_NOT_EXIST}")
@users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}")
@users_ns.route("user/personal_details")
class MyProfilePersonalDetails(Resource):
    @classmethod
    @users_ns.doc("get_user_personal_details")
    @users_ns.response(HTTPStatus.OK, "Successful request", full_user_api_model)
    @users_ns.expect(auth_header_parser, validate=True)
    def get(cls):
        """
        Returns personal details of current user.

        A user with valid access token can use this endpoint to view their own
        user details. The endpoint doesn't take any other input.
        """
        token = request.headers.environ["HTTP_AUTHORIZATION"]

        return http_response_checker(get_request("/user", token))


    @classmethod
    @users_ns.doc("update_user_personal_details")
    @users_ns.response(HTTPStatus.OK, f"{messages.USER_SUCCESSFULLY_UPDATED}")
    @users_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input.")
    @users_ns.expect(auth_header_parser, update_user_details_request_body_model, validate=True,)
    def put(cls):
        """
        Updates user personal details

        A user with valid access token can use this endpoint to edit their own
        user details. The endpoint takes any of the given parameters (name, username,
        bio, location, occupation, organization, slack_username, social_media_links,
        skills, interests, resume_url, photo_url, need_mentoring, available_to_mentor).
        The response contains a success or error message.
        """

        data = request.json
        
        if not data:
            return messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT

        is_field_valid = expected_fields_validator(data, update_user_details_request_body_model)
        if not is_field_valid.get("is_field_valid"):
            return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST
        
        is_not_valid = validate_update_profile_request_data(data)
        if is_not_valid:
            return is_not_valid, HTTPStatus.BAD_REQUEST

        token = request.headers.environ["HTTP_AUTHORIZATION"]
        
        return http_response_checker(put_request("/user", token, data))

    
@users_ns.response( 
        HTTPStatus.UNAUTHORIZED,
    f"{messages.TOKEN_HAS_EXPIRED}\n"
    f"{messages.TOKEN_IS_INVALID}\n"
    f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
)
@users_ns.response(
        HTTPStatus.FORBIDDEN, f"{messages.USER_ID_IS_NOT_RETRIEVED}"
)
@users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}")
@users_ns.route("user/additional_info")
class MyProfileAdditionalInfo(Resource):
    @classmethod
    @users_ns.doc("get_user_additional_info")
    @users_ns.response(HTTPStatus.OK, "Successful request", get_user_extension_response_model)
    @users_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input.")
    @users_ns.response(HTTPStatus.NOT_FOUND, f"{messages.ADDITIONAL_INFORMATION_DOES_NOT_EXIST}")
    @users_ns.expect(auth_header_parser, validate=True)
    def get(cls):
        """
        Returns additional information of current user

        A user with valid access token can use this endpoint to view their additional information details. 
        The endpoint doesn't take any other input. But the user must get their personal details first 
        before they can send this request for getting the additional information.
        """

        token = request.headers.environ["HTTP_AUTHORIZATION"]

        is_wrong_token = validate_token(token)

        if not is_wrong_token:
            try:
                user_id = AUTH_COOKIE["user_id"].value
            except KeyError:
                return messages.USER_ID_IS_NOT_RETRIEVED, HTTPStatus.FORBIDDEN
                
            result = UserExtensionDAO.get_user_additional_data_info(user_id)
            if not result:
                return messages.ADDITIONAL_INFORMATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
            return result 
        return is_wrong_token
    

    @classmethod
    @users_ns.doc("create_user_additional_info")
    @users_ns.doc(
        responses={
            HTTPStatus.INTERNAL_SERVER_ERROR: f"{messages.INTERNAL_SERVER_ERROR['message']}"
        }
    )
    @users_ns.response(
        HTTPStatus.CREATED, f"{messages.ADDITIONAL_INFO_SUCCESSFULLY_CREATED}"
    )
    @users_ns.response(
        HTTPStatus.BAD_REQUEST,
        f"{messages.USER_ID_IS_NOT_VALID}\n"
        f"{messages.IS_ORGANIZATION_REP_FIELD_IS_MISSING}\n"
        f"{messages.TIMEZONE_FIELD_IS_MISSING}"
        f"{messages.UNEXPECTED_INPUT}"
    )
    @users_ns.response(
        HTTPStatus.FORBIDDEN, f"{messages.USER_ID_IS_NOT_RETRIEVED}"
    )
    @users_ns.response(
        HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}"
    )
    @users_ns.expect(auth_header_parser, user_extension_request_body_model, validate=True)
    def post(cls):
        """
        Creates user additional information

        A user with valid access token can use this endpoint to add additional information to their own data. 
        The endpoint takes any of the given parameters (is_organization_rep (true or false value), timezone 
        (with value as per Timezone Enum Name) and additional_info (dictionary of phone, mobile and personal_website)).
        The response contains a success or error message. This request only accessible once user confirm 
        their additional information have not already exist in the data through sending GET request for 
        additional information.
        """

        token = request.headers.environ["HTTP_AUTHORIZATION"]
        is_wrong_token = validate_token(token)
        
        if not is_wrong_token:
            data = request.json
            if not data:
                return messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT

            is_field_valid = expected_fields_validator(data, user_extension_request_body_model)
            if not is_field_valid.get("is_field_valid"):
                return is_field_valid.get("message"), HTTPStatus.BAD_REQUEST
            
            is_not_valid = validate_update_additional_info_request(data)
            if is_not_valid:
                return is_not_valid, HTTPStatus.BAD_REQUEST

            return UserExtensionDAO.create_user_additional_info(data)
             
        return is_wrong_token
    