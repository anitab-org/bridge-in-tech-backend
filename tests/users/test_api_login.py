import unittest
from http import HTTPStatus
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.ms_api_utils import post_request, BASE_MS_API_URL
from app.api.resources.users import LoginUser
from tests.test_data import user1


mock_response = Mock()
mock_error = Mock()

user_login_success = {
    "username": user1.get("username"),
    "password": user1.get("password")
}

user_wrong_data = {
        "username": "user_wrong_data",
        "password": "user_wrong_data",
    }


class TestUserLoginApi(BaseTestCase):
    def send_success_request(self, data, expected_code, expected_message, mock_login):
        mock_response.json.return_value = expected_message
        mock_response.status_code = expected_code
        mock_login.return_value = mock_response
        mock_login.raise_for_status = json.dumps(expected_code)
        return post_login(self, data)
        
    def send_http_error_request(self, data, expected_code, expected_message, mock_login):
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_login.return_value = mock_response
        mock_error.json.return_value = expected_message
        mock_error.status_code = expected_code
        mock_login.side_effect = requests.exceptions.HTTPError(response=mock_error)
        return post_login(self, data)

    @patch("requests.post")
    def test_api_login_successful(self, mock_login):
        success_message = {"access_token": "this is fake token", "access_expiry": 1593144238}
        success_code = HTTPStatus.OK
        response = self.send_success_request(user_login_success, success_code, success_message, mock_login)
        check_assert(self, response, success_message, success_code, mock_login)
    
    @patch("requests.post")
    def test_api_wrong_password(self, mock_login):
        error_message = messages.WRONG_USERNAME_OR_PASSWORD
        error_code = HTTPStatus.UNAUTHORIZED
        response = self.send_http_error_request(user_wrong_data, error_code, error_message, mock_login)
        check_assert(self, response, error_message, error_code, mock_login)
    
    @patch("requests.post")
    def test_api_internal_server_error(self, mock_login):
        error_message = messages.INTERNAL_SERVER_ERROR
        error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response = self.send_http_error_request(user_login_success, error_code, error_message, mock_login)
        check_assert(self, response, error_message, error_code, mock_login)


def post_login(self, user_data):
    with self.client:
        response = self.client.post(
            "/login",
            data=json.dumps(user_data),
            follow_redirects=True,
            content_type="application/json",
        )
    return response
    
def check_assert(self, response, message, response_code, mock_login):
    mock_login.assert_called()
    self.assertEqual(response.json, message)
    self.assertEqual(response.status_code, response_code)
   
    
if __name__ == "__main__":
    unittest.main()
