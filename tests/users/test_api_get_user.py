import unittest
from http import HTTPStatus, cookies
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from flask_restx import marshal
from app import messages
from tests.base_test_case import BaseTestCase
from app.api.ms_api_utils import post_request, BASE_MS_API_URL, AUTH_COOKIE
from app.api.resources.users import MyProfilePersonalDetails
from app.api.models.user import full_user_api_model
from tests.test_data import user1


class TestGetUserApi(BaseTestCase):
    
    @patch("requests.get")
    @patch("requests.post")
    def test_api_get_user_with_correct_token(self, mock_login, mock_get_user):
        success_message = {"access_token": "this is fake token", "access_expiry": 1601478236}
        success_code = HTTPStatus.OK

        mock_login_response = Mock()
        mock_login_response.json.return_value = success_message
        mock_login_response.status_code = success_code
        mock_login.return_value = mock_login_response
        mock_login.raise_for_status = json.dumps(success_code)

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
      
        access_token_header = "Bearer this is fake token"
        expected_user = marshal(user1, full_user_api_model)
        success_code = HTTPStatus.OK

        mock_get_response = Mock()
        mock_get_response.json.return_value = expected_user
        mock_get_response.status_code = success_code

        mock_get_user.return_value = mock_get_response
        mock_get_user.raise_for_status = json.dumps(success_code)

        with self.client:
            get_response = self.client.get(
                "/user/personal_details",
                headers={"Authorization": access_token_header},
                follow_redirects=True,
            )
            
        mock_get_user.assert_called()
        self.assertEqual(get_response.json, expected_user)
        self.assertEqual(get_response.status_code, success_code)


    @patch("requests.get")
    @patch("requests.post")
    def test_api_get_user_with_token_expired(self, mock_login, mock_get_user):
        success_message = {"access_token": "this is fake token", "access_expiry": 1593144238}
        success_code = HTTPStatus.OK

        mock_login_response = Mock()
        mock_login_response.json.return_value = success_message
        mock_login_response.status_code = success_code
        mock_login.return_value = mock_login_response
        mock_login.raise_for_status = json.dumps(success_code)

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
      
        access_token_header = "Bearer this is fake token"

        error_message = messages.TOKEN_HAS_EXPIRED
        error_code = HTTPStatus.UNAUTHORIZED

        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_get_user.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_get_user.side_effect = requests.exceptions.HTTPError(response=mock_error)

        with self.client:
            get_response = self.client.get(
                "/user/personal_details",
                headers={"Authorization": access_token_header},
                follow_redirects=True,
            )
            
        mock_get_user.assert_not_called()
        self.assertEqual(get_response.json, error_message)
        self.assertEqual(get_response.status_code, error_code)


    @patch("requests.get")
    def test_api_get_user_with_internal_server_error(self, mock_get_user):

        access_token_header = "Bearer this is fake token"
        error_message = messages.INTERNAL_SERVER_ERROR
        error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        
        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_get_user.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_get_user.side_effect = requests.exceptions.HTTPError(response=mock_error)
        
        with self.client:
            get_response = self.client.get(
                "/user/personal_details",
                headers={"Authorization": access_token_header},
                follow_redirects=True,
            )
            
        mock_get_user.assert_called()
        self.assertEqual(get_response.json, error_message)
        self.assertEqual(get_response.status_code, error_code)


if __name__ == "__main__":
    unittest.main()

   