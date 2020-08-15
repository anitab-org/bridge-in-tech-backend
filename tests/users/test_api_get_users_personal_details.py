import unittest
from http import HTTPStatus, cookies
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from flask_restx import marshal
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.request_api_utils import post_request, get_request, BASE_MS_API_URL, AUTH_COOKIE
from app.api.models.user import full_user_api_model, get_user_extension_response_model
from tests.test_data import user1, user2, user3
from app.database.models.ms_schema.user import UserModel
from app.api.models.user import public_user_personal_details_response_model


class TestGetUsersListPersonalDetailsApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestGetUsersListPersonalDetailsApi, self).setUp()
        
        # The access_expiry on this test is set to Wednesday, 30-Sep-20 15:03:56 UTC.
        # This date need to be adjusted accordingly once the development is near/pass the stated date
        # to make sure the test still pass.
        success_message = {"access_token": "this is fake token", "access_expiry": 1601478236}
        success_code = HTTPStatus.OK

        mock_login_response = Mock()
        mock_login_response.json.return_value = success_message
        mock_login_response.status_code = success_code
        mock_login.return_value = mock_login_response
        mock_login.raise_for_status = json.dumps(success_code)

        expected_user = marshal(user1, full_user_api_model)
        
        mock_get_response = Mock()
        mock_get_response.json.return_value = expected_user
        mock_get_response.status_code = success_code

        mock_get_user.return_value = mock_get_response
        mock_get_user.raise_for_status = json.dumps(success_code)
        
        user_login_success = {
            "username": user1.get("username"),
            "password": user1.get("password")
        }
        
        with self.client:
            login_response = self.client.post(
                "/login",
                data=json.dumps(user_login_success),
                follow_redirects=True,
                content_type="application/json",
            )

        test_user1 = UserModel(
            name=user1["name"],
            username=user1["username"],
            password=user1["password"], 
            email=user1["email"], 
            terms_and_conditions_checked=user1["terms_and_conditions_checked"]
        )
        test_user1.need_mentoring = user1["need_mentoring"]
        test_user1.available_to_mentor = user1["available_to_mentor"]

        test_user1.save_to_db()
        test_user1_data = UserModel.find_by_email(test_user1.email)
        AUTH_COOKIE["user"] = marshal(test_user1_data, full_user_api_model)
        
        
    @patch("requests.get")
    def test_api_list_users_personal_details_with_correct_token(self, mock_get_users):
        test_user2 = UserModel(
            name=user2["name"],
            username=user2["username"],
            password=user2["password"], 
            email=user2["email"], 
            terms_and_conditions_checked=user2["terms_and_conditions_checked"]
        )
        test_user2.need_mentoring = user2["need_mentoring"]
        test_user2.available_to_mentor = user2["available_to_mentor"]
        test_user2.is_email_verified = True

        test_user3 = UserModel(
            name=user3["name"],
            username=user3["username"],
            password=user3["password"], 
            email=user3["email"], 
            terms_and_conditions_checked=user3["terms_and_conditions_checked"]
        )
        test_user3.need_mentoring = user3["need_mentoring"]
        test_user3.available_to_mentor = user3["available_to_mentor"]
        test_user3.is_email_verified = True
        
        test_user2.save_to_db()
        test_user3.save_to_db()
        
        test_user2_data = UserModel.find_by_email(test_user2.email)
        test_user3_data = UserModel.find_by_email(test_user3.email)

        expected_list = [
            marshal(test_user2_data, public_user_personal_details_response_model),
            marshal(test_user3_data, public_user_personal_details_response_model)
        ]
        success_code = HTTPStatus.OK

        mock_get_response = Mock()
        mock_get_response.json.return_value = expected_list
        mock_get_response.status_code = success_code

        mock_get_users.return_value = mock_get_response
        mock_get_users.raise_for_status = json.dumps(success_code)

        with self.client:
            get_response = self.client.get(
                "/users",
                headers={
                    "Authorization": AUTH_COOKIE["Authorization"].value,
                    "search": "",
                    "page": None,
                    "per_page": None,
                    "Accept": "application/json"
                }, 
                follow_redirects=True,
            )

        mock_get_users.assert_called()
        self.assertEqual(get_response.json, expected_list)
        self.assertEqual(get_response.status_code, success_code)

    
    @patch("requests.get")
    def test_api_list_users_personal_details_with_token_expired(self, mock_get_users):
        error_message = messages.TOKEN_HAS_EXPIRED
        error_code = HTTPStatus.UNAUTHORIZED

        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_get_users.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_get_users.side_effect = requests.exceptions.HTTPError(response=mock_error)

        with self.client:
            get_response = self.client.get(
                "/users",
                headers={
                    "Authorization": AUTH_COOKIE["Authorization"].value,
                    "search": "",
                    "page": None,
                    "per_page": None,
                    "Accept": "application/json"
                }, 
                follow_redirects=True,
            )
        
        mock_get_users.assert_called()
        self.assertEqual(get_response.json, error_message)
        self.assertEqual(get_response.status_code, error_code)
