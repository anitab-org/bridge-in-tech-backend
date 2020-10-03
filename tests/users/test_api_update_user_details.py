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
from app.api.models.user import update_user_details_request_body_model
from tests.test_data import user1



class TestUpdateUserDetailsApi(BaseTestCase):
    
    @patch("requests.post")
    def setUp(self, mock_login):
        super(TestUpdateUserDetailsApi, self).setUp()
        # set access expiry 4 weeks from today's date (sc*min*hrrs*days)
        access_expiry = time.time() + 60*60*24*28
        success_login_message = {"access_token": "this is fake token", "access_expiry": access_expiry}
        success_login_code = HTTPStatus.OK

        mock_login_response = Mock()
        mock_login_response.json.return_value = success_login_message
        mock_login_response.status_code = success_login_code
        mock_login.return_value = mock_login_response
        mock_login.raise_for_status = json.dumps(success_login_code)

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
      
        self.access_token_header = "Bearer this is fake token"
        self.user_new_details = {
            "name": "test update",
            "username": "testupdate",
            "bio": "string",
            "location": "string",
            "occupation": "string",
            "current_organization": "string",
            "slack_username": "string",
            "social_media_links": "string",
            "skills": "string",
            "interests": "string",
            "resume_url": "string",
            "photo_url": "string",
            "need_mentoring": True,
            "available_to_mentor": True
        }
    

    @patch("requests.put")
    def test_api_update_user_details_with_correct_payload(self, mock_update_user):
        expected_put_message = messages.USER_SUCCESSFULLY_UPDATED
        expected_put_code = HTTPStatus.OK

        mock_update_response = Mock()
        mock_update_response.json.return_value = expected_put_message
        mock_update_response.status_code = expected_put_code

        mock_update_user.return_value = mock_update_response
        mock_update_user.raise_for_status = json.dumps(expected_put_code)

        with self.client:
            put_response = self.client.put(
                "/user/personal_details",
                data=json.dumps(self.user_new_details),
                content_type="application/json",
                headers={"Authorization": self.access_token_header},
                follow_redirects=True,
            )
            
        mock_update_user.assert_called()
        self.assertEqual(put_response.json, expected_put_message)
        self.assertEqual(put_response.status_code, expected_put_code)


    @patch("requests.put")
    def test_api_update_user_details_with_new_username_invalid(self, mock_update_user):
        user_invalid_details = {
            "name": "test update",
            "username": "testupdate?",
            "bio": "string",
            "location": "string",
            "occupation": "string",
            "current_organization": "string",
            "slack_username": "string",
            "social_media_links": "string",
            "skills": "string",
            "interests": "string",
            "resume_url": "string",
            "photo_url": "string",
            "need_mentoring": True,
            "available_to_mentor": True
        }
        
        error_message = messages.NEW_USERNAME_INPUT_BY_USER_IS_INVALID
        error_code = HTTPStatus.BAD_REQUEST

        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_update_user.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_update_user.side_effect = requests.exceptions.HTTPError(response=mock_error)

        with self.client:
            put_response = self.client.put(
                "/user/personal_details",
                data=json.dumps(user_invalid_details),
                content_type="application/json",
                headers={"Authorization": self.access_token_header},
                follow_redirects=True,
            )
            
        mock_update_user.assert_not_called()
        self.assertEqual(put_response.json, error_message)
        self.assertEqual(put_response.status_code, error_code)


    @patch("requests.put")
    def test_api_update_user_details_with_internal_server_error(self, mock_update_user):

        error_message = messages.INTERNAL_SERVER_ERROR
        error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        
        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_update_user.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_update_user.side_effect = requests.exceptions.HTTPError(response=mock_error)
        
        with self.client:
            put_response = self.client.put(
                "/user/personal_details",
                data=json.dumps(self.user_new_details),
                content_type="application/json",
                headers={"Authorization": self.access_token_header},
                follow_redirects=True,
            )
            
        mock_update_user.assert_called()
        self.assertEqual(put_response.json, error_message)
        self.assertEqual(put_response.status_code, error_code)


if __name__ == "__main__":
    unittest.main()

   