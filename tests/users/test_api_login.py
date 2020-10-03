import time
import unittest
from http import HTTPStatus
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from flask_restx import marshal
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.request_api_utils import post_request, BASE_MS_API_URL
from app.api.resources.users import LoginUser
from app.api.models.user import full_user_api_model
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from tests.test_data import user1


class TestUserLoginApi(BaseTestCase):
    def setUp(self):
        super(TestUserLoginApi, self).setUp()

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
        self.test_user1_data = UserModel.find_by_email(test_user1.email)
        self.expected_user = marshal(self.test_user1_data, full_user_api_model)
        
    
    @patch("requests.get")
    @patch("requests.post")
    def test_api_login_successful(self, mock_login, mock_get_user):
        # set access expiry 4 weeks from today's date (sc*min*hrrs*days)
        access_expiry = time.time() + 60*60*24*28
        success_message = {"access_token": "this is fake token", "access_expiry": access_expiry}
        success_code = HTTPStatus.OK

        mock_response = Mock()
        mock_response.json.return_value = success_message
        mock_response.status_code = success_code
        mock_login.return_value = mock_response
        mock_login.raise_for_status = json.dumps(success_code)

        user_login_success = {
            "username": user1.get("username"),
            "password": user1.get("password")
        }

        expected_user = marshal(user1, full_user_api_model)
        
        mock_get_response = Mock()
        mock_get_response.json.return_value = expected_user
        mock_get_response.status_code = success_code

        mock_get_user.return_value = mock_get_response
        mock_get_user.raise_for_status = json.dumps(success_code)
        
        with self.client:
            response = self.client.post(
                "/login",
                data=json.dumps(user_login_success),
                follow_redirects=True,
                content_type="application/json",
            )
        
        mock_login.assert_called()
        self.assertEqual(response.json, success_message)
        self.assertEqual(response.status_code, success_code)


    @patch("requests.post")
    def test_api_wrong_password(self, mock_login):
        error_message = messages.WRONG_USERNAME_OR_PASSWORD
        error_code = HTTPStatus.UNAUTHORIZED
        
        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_login.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_login.side_effect = requests.exceptions.HTTPError(response=mock_error)

        user_wrong_data = {
            "username": "user_wrong_data",
            "password": "user_wrong_data",
        }

        with self.client:
            response = self.client.post(
                "/login",
                data=json.dumps(user_wrong_data),
                follow_redirects=True,
                content_type="application/json",
            )
       
        mock_login.assert_called()
        self.assertEqual(response.json, error_message)
        self.assertEqual(response.status_code, error_code)
    

    @patch("requests.post")
    def test_api_internal_server_error(self, mock_login):
        error_message = messages.INTERNAL_SERVER_ERROR
        error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        
        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_login.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_login.side_effect = requests.exceptions.HTTPError(response=mock_error)

        
        user_server_error = {
             "username": "user_server_error",
            "password": "user_server_error",
        }
        with self.client:
            response = self.client.post(
                "/login",
                data=json.dumps(user_server_error),
                follow_redirects=True,
                content_type="application/json",
            )
       
        mock_login.assert_called()
        self.assertEqual(response.json, error_message)
        self.assertEqual(response.status_code, error_code)
    

if __name__ == "__main__":
    unittest.main()

   