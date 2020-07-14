import unittest
from http import HTTPStatus
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.request_api_utils import post_request, BASE_MS_API_URL
from app.api.resources.users import UserRegister
from tests.test_data import user1

class TestUserRegistrationApi(BaseTestCase):

    @patch("requests.post")
    def test_api_register_successful(self, mock_register):
        
        response_code = HTTPStatus.CREATED
        expected_message = messages.USER_WAS_CREATED_SUCCESSFULLY
        
        mock_response = Mock()
        mock_response.json.return_value = expected_message
        mock_response.status_code = HTTPStatus.CREATED
        mock_register.return_value = mock_response
        mock_register.raise_for_status = json.dumps(HTTPStatus.CREATED)
        
        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(user1),
                follow_redirects=True,
                content_type="application/json",
            )

        mock_register.assert_called()
        self.assertEqual(1, mock_register.call_count)
        self.assertEqual(response.json, expected_message)
        self.assertEqual(response.status_code, response_code)
        
     
    @patch("requests.post")
    def test_api_register_password_invalid(self, mock_register):
        
        response_code = HTTPStatus.BAD_REQUEST
        expected_message = messages.PASSWORD_INPUT_BY_USER_HAS_INVALID_LENGTH

        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_register.return_value = mock_response
        
        mock_error = Mock()
        mock_error.json.return_value = expected_message
        mock_error.status_code = response_code
        mock_register.side_effect = requests.exceptions.HTTPError(response=mock_error)

        user_invalid_pwd = {
            "name": "user pwd invalid",
            "username": "username_pwd_invalid",
            "password": "toshort",
            "email": "email@pwd.invalid",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }

        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(user_invalid_pwd),
                follow_redirects=True,
                content_type="application/json",
            )
        
        mock_register.assert_not_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response.json, expected_message)
        self.assertEqual(response.status_code, response_code)
        
    
    @patch("requests.post")
    def test_api_register_username_exist(self, mock_register):
        
        response_code = HTTPStatus.CONFLICT
        expected_message = messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS

        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_register.return_value = mock_response
        
        user_username_exist = {
            "name": "user username exist",
            "username": "username_exist",
            "password": "pwd_username_exist",
            "email": "email@username.exist",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }

        mock_error = Mock()
        mock_error.json.return_value = expected_message
        mock_error.status_code = response_code
        mock_register.side_effect = requests.exceptions.HTTPError(response=mock_error)

        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(user_username_exist),
                follow_redirects=True,
                content_type="application/json",
            )

        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response.json, expected_message)
        self.assertEqual(response.status_code, response_code)
        
        
    @patch("requests.post")
    def test_api_register_email_exist(self, mock_register):
        
        response_code = HTTPStatus.CONFLICT
        expected_message = messages.USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS
        
        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_register.return_value = mock_response

        mock_error = Mock()
        mock_error.json.return_value = expected_message
        mock_error.status_code = response_code
        mock_register.side_effect = requests.exceptions.HTTPError(response=mock_error)

        user_email_exist = {
            "name": "user email exist",
            "username": "username_email_exist",
            "password": "pwd_email_exist",
            "email": "user@email.exist",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }

        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(user_email_exist),
                follow_redirects=True,
                content_type="application/json",
            )

        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response.json, expected_message)
        self.assertEqual(response.status_code, response_code)
        

    @patch("requests.post")
    def test_api_register_internal_server_error(self, mock_register):
        
        response_code = HTTPStatus.INTERNAL_SERVER_ERROR
        expected_message = messages.INTERNAL_SERVER_ERROR
        
        mock_response = Mock()
        server_error = Exception()
        mock_response.raise_for_status.side_effect = server_error
        mock_register.return_value = mock_response

        mock_error = Mock()
        mock_error.json.return_value = expected_message
        mock_error.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_register.side_effect = Exception()
        
        user_server_err = {
            "name": "user server err",
            "username": "username_server_err",
            "password": "pwd_server_err",
            "email": "email@server.err",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }
        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(user_server_err),
                follow_redirects=True,
                content_type="application/json",
            )
            
        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response.json, expected_message)
        self.assertEqual(response.status_code, response_code)
        
               
if __name__ == "__main__":
    unittest.main()
