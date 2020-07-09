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
from app.api.ms_api_utils import post_request, get_request, http_response_checker, AUTH_COOKIE
from app import messages
from app.api.models.user import *
from app.api.validations.user import *
from app.api.resources.common import auth_header_parser

users_ns = Namespace("Users", description="Operations related to users")
add_models_to_namespace(users_ns)


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
        f"{messages.TERMS_AND_CONDITIONS_ARE_NOT_CHECKED}"
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
        available_to_mentor(true/false)) and Bridge In Tech API (is_organization_rep and timezone).
        A success message is displayed and verification email is sent to the user's email ID.
        """

        data = request.json

        is_valid = validate_user_registration_request_data(data)

        if is_valid != {}:
            return is_valid, HTTPStatus.BAD_REQUEST
            
        result = post_request("/register", data)

        return http_response_checker(result)

        
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

        if not username:
            return messages.USERNAME_FIELD_IS_MISSING, HTTPStatus.BAD_REQUEST
        if not password:
            return messages.PASSWORD_FIELD_IS_MISSING, HTTPStatus.BAD_REQUEST

        result = post_request("/login", data)

        return http_response_checker(result)
        

@users_ns.route("user/personal_details")
class MyProfilePersonalDetails(Resource):
    @classmethod
    @users_ns.doc("get_user")
    @users_ns.response(HTTPStatus.OK, "Successful request", full_user_api_model)
    @users_ns.response(
        HTTPStatus.UNAUTHORIZED,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
    )
    @users_ns.response(HTTPStatus.NOT_FOUND, f"{messages.USER_DOES_NOT_EXIST}")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, f"{messages.INTERNAL_SERVER_ERROR}")
    @users_ns.expect(auth_header_parser, validate=True)
    def get(cls):
        """
        Returns details of current user.

        A user with valid access token can use this endpoint to view his/her own
        user details. The endpoint doesn't take any other input.
        """
        token = request.headers.environ["HTTP_AUTHORIZATION"]
        
        result = get_request("/user", token)
        return http_response_checker(result)
