import unittest
from http import HTTPStatus
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.ms_api_utils import post_request, BASE_MS_API_URL
from app.api.resources.users import UserRegister
from tests.test_data import user1

class TestUserRegistrationApi(BaseTestCase):

    @patch("requests.post")
    def test_api_register_successful(self, mock_register):
        
        json_response_code = json.dumps(HTTPStatus.CREATED)
        message = {'message': f'{messages.USER_WAS_CREATED_SUCCESSFULLY}'}
        status_code = {'status_code': f"{json_response_code}"}
        expected_tuple = [message, status_code]
        
        mock_response = Mock()
        mock_response.json.return_value = expected_tuple
        mock_register.return_value = mock_response

        data = user1
        response = post_request(f"{BASE_MS_API_URL}/register", data)

        mock_register.assert_called()
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(response[0], expected_tuple)
        

    @patch("requests.post")
    def test_api_register_password_invalid(self, mock_register):
        
        json_response_code = json.dumps(HTTPStatus.BAD_REQUEST)
        message = {'message': f'{messages.PASSWORD_INPUT_BY_USER_HAS_INVALID_LENGTH}'}
        status_code = {'status_code': f"{json_response_code}"}
        expected_tuple = [message, status_code]
        
        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_register.return_value = mock_response
        
        mock_error = Mock()
        mock_error.json.return_value = expected_tuple
        mock_register.side_effect = requests.exceptions.HTTPError(response=mock_error)

        data = {
            "name": "user_pwd_invalid",
            "username": "username_pwd_invalid",
            "password": "toshort",
            "email": "email_pwd_invalid",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }
        response = post_request(f"{BASE_MS_API_URL}/register", data)
        
        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response[0], expected_tuple)
        

    @patch("requests.post")
    def test_api_register_username_exist(self, mock_register):
        
        json_response_code = json.dumps(HTTPStatus.CONFLICT)
        message = {'message': '{messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS}'}
        status_code = {'status_code': f"{json_response_code}"}
        expected_tuple = [message, status_code]

        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_register.return_value = mock_response
        
        mock_error = Mock()
        mock_error.json.return_value = expected_tuple
        mock_register.side_effect = requests.exceptions.HTTPError(response=mock_error)
        
        data = {
            "name": "user_username_exist",
            "username": "username_exist",
            "password": "pwd_username_exist",
            "email": "email_username_exist",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }
        response = post_request(f"{BASE_MS_API_URL}/register", data)
        
        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response[0], expected_tuple)

        
    @patch("requests.post")
    def test_api_register_email_exist(self, mock_register):
        
        json_response_code = json.dumps(HTTPStatus.CONFLICT)
        message = {'message': '{messages.USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS}'}
        status_code = {'status_code': f"{json_response_code}"}
        expected_tuple = [message, status_code]

        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_register.return_value = mock_response

        mock_error = Mock()
        mock_error.json.return_value = expected_tuple
        mock_register.side_effect = requests.exceptions.HTTPError(response=mock_error)

        data = {
            "name": "user_email_exist",
            "username": "username_email_exist",
            "password": "pwd_email_exist",
            "email": "email_exist",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }
        response = post_request(f"{BASE_MS_API_URL}/register", data)
        
        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response[0], expected_tuple)
        

    @patch("requests.post")
    def test_api_register_internal_server_error(self, mock_register):
        
        json_response_code = json.dumps(HTTPStatus.INTERNAL_SERVER_ERROR)
        json_response_message = messages.INTERNAL_SERVER_ERROR
        message = json_response_message
        status_code = f"{json_response_code}"
        expected_tuple = [message, status_code]
        
        mock_response = Mock()
        server_error = Exception()
        mock_response.raise_for_status.side_effect = server_error
        mock_register.return_value = mock_response

        mock_error = Mock()
        mock_error.json.return_value = expected_tuple
        mock_register.side_effect = Exception()
        
        data = {
            "name": "user_server_err",
            "username": "username_server_err",
            "password": "pwd_server_err",
            "email": "email_server_err",
            "terms_and_conditions_checked": True,
            "need_mentoring": True,
            "available_to_mentor": False,
        }
        response = post_request(f"{BASE_MS_API_URL}/register", data)
        
        mock_register.assert_called()
        self.assertEqual(0, mock_response.raise_for_status.call_count)
        self.assertEqual(0, mock_register.json.call_count)
        self.assertEqual(0, mock_register.raise_for_status.call_count)
        self.assertEqual(response[0], expected_tuple[0])
        self.assertEqual(response[1], expected_tuple[1])
    
               
if __name__ == "__main__":
    unittest.main()
