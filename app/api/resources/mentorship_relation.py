import ast
import json
from flask import request
from flask_restx import Resource, Namespace, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from app import messages
from app.api.request_api_utils import (
    post_request, 
    get_request,
    put_request, 
    http_response_checker, 
    AUTH_COOKIE, 
    validate_token)
from app.api.resources.common import auth_header_parser
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.api.dao.user_extension import UserExtensionDAO
from app.api.models.mentorship_relation import *
from app.utils.validation_utils import get_length_validation_error_message
from app.database.models.bit_schema.mentorship_relation_extension import MentorshipRelationExtensionModel
from app.utils.ms_constants import DEFAULT_PAGE, DEFAULT_USERS_PER_PAGE

mentorship_relation_ns = Namespace(
    "Mentorship Relation",
    description="Operations related to " "mentorship relations " "between users",
)
add_models_to_namespace(mentorship_relation_ns)

DAO = MentorshipRelationDAO()
UserExtensionDAO = UserExtensionDAO()


@mentorship_relation_ns.route("mentorship_relations")
class GetAllMyMentorshipRelation(Resource):
    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc("get_all_user_mentorship_relations")
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.param(
        name="relation_state",
        description="Mentorship relation state filter.",
        _in="query",
    )
    @mentorship_relation_ns.response(
        HTTPStatus.OK,
        "Return all user's mentorship relations, filtered by the relation state, was successfully.",
        model=mentorship_request_response_body,
    )
    @mentorship_relation_ns.response(
        HTTPStatus.UNAUTHORIZED,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}"
    )
    @mentorship_relation_ns.marshal_list_with(mentorship_request_response_body)
    def get(cls):
        """
        Lists all mentorship relations of current user.

        Input:
        1. Header: valid access token

        Returns:
        JSON array containing user's relations as objects.
        """

        user_id = get_jwt_identity()
        rel_state_param = request.args
        rel_state_filter = None

        if rel_state_param:
            rel_state_filter = rel_state_param["relation_state"].upper()

        response = DAO.list_mentorship_relations(
            user_id=user_id, state=rel_state_filter
        )

        return response
