import json
from http import HTTPStatus
from flask import request
from flask_restx import Resource, Namespace
from app.api.ms_api_utils import post_request, BASE_MS_API_URL
from app import messages
from app.api.models.user import *

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
        f"{messages.PASSWORD_INPUT_BY_USER_HAS_INVALID_LENGTH}"
    )
    @users_ns.response(
        HTTPStatus.CONFLICT,
        f"{messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS}\n"
        f"{messages.USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS}",
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

        # send POST /register request to MS API and return response
        
        result = post_request(f"{BASE_MS_API_URL}/register", data)

        if result[1] == HTTPStatus.OK:
            return f"{messages.USER_WAS_CREATED_SUCCESSFULLY}", HTTPStatus.CREATED
        elif result[1] == HTTPStatus.INTERNAL_SERVER_ERROR:
            return f"{messages.INTERNAL_SERVER_ERROR}", HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            return result
