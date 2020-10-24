import ast
import time
import unittest
from http import HTTPStatus, cookies
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from flask_restx import marshal
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.request_api_utils import post_request, BASE_MS_API_URL, AUTH_COOKIE
from app.api.resources.users import MyProfilePersonalDetails
from app.api.models.user import full_user_api_model
from tests.test_data import user1


class TestGetUserDetailsApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestGetUserDetailsApi, self).setUp()
        # set access expiry 4 weeks from today's date (sc*min*hrrs*days)
        access_expiry = time.time() + 60*60*24*28
        success_message = {"access_token": "this is fake token", "access_expiry": access_expiry}
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
      

    def test_api_get_user_details_with_correct_token(self):
      
        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        success_code = HTTPStatus.OK

        with self.client:
            get_response = self.client.get(
                "/user/personal_details",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                follow_redirects=True,
            )
            
        self.assertEqual(get_response.json, user)
        self.assertEqual(get_response.status_code, success_code)


    @patch("requests.get")
    def test_api_get_user_details_with_incorrect_token(self, mock_get_user):
        error_message = messages.TOKEN_IS_INVALID
        error_code = HTTPStatus.UNAUTHORIZED

        with self.client:
            get_response = self.client.get(
                "/user/personal_details",
                headers={"Authorization": "Bearer Token incorrect"},
                follow_redirects=True,
            )
            
        self.assertEqual(get_response.json, error_message)
        self.assertEqual(get_response.status_code, error_code)


if __name__ == "__main__":
    unittest.main()

   