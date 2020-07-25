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
from tests.test_data import user1
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel


class TestGetUserAdditionalInfoApi(BaseTestCase):
    
    @patch("requests.post")
    def setUp(self, mock_login):
        super(TestGetUserAdditionalInfoApi, self).setUp()

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
        
        test_user = UserModel(
            name=user1["name"],
            username=user1["username"],
            password=user1["password"], 
            email=user1["email"], 
            terms_and_conditions_checked=user1["terms_and_conditions_checked"]
        )
        test_user.need_mentoring = user1["need_mentoring"]
        test_user.available_to_mentor = user1["available_to_mentor"]

        test_user.save_to_db()

        self.test_user_data = UserModel.find_by_email(test_user.email)

        AUTH_COOKIE["user_id"] = self.test_user_data.id

        self.response_additional_info = {
            "user_id": self.test_user_data.id,
            "is_organization_rep": True,
            "timezone": "UTC-01:00/Cape Verde Time",
            "phone": "123-456-789",
            "mobile": "",
            "personal_website": ""
        }
        
        
    @patch("requests.get")
    def test_api_dao_get_user_additional_info_successfully(self, mock_get_additional_info):
        success_message = self.response_additional_info
        success_code = HTTPStatus.OK

        mock_get_response = Mock()
        mock_get_response.json.return_value = success_message
        mock_get_response.status_code = success_code

        mock_get_additional_info.return_value = mock_get_response
        mock_get_additional_info.raise_for_status = json.dumps(success_code)

        # prepare existing additional info
        additional_info = {
            "phone": self.response_additional_info["phone"],
            "mobile": self.response_additional_info["mobile"],
            "personal_website": self.response_additional_info["personal_website"]
        }

        user_extension = UserExtensionModel(
            self.response_additional_info["user_id"], 
            "CAPE_VERDE_TIME",
        )
        user_extension.is_organization_rep = self.response_additional_info["is_organization_rep"]
        user_extension.additional_info = additional_info
        
        user_extension.save_to_db()
        
        with self.client:
            response = self.client.get(
                "/user/additional_info",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                follow_redirects=True,
                content_type="application/json",
            )
    
        test_user_additional_info_data = UserExtensionModel.query.filter_by(user_id=self.test_user_data.id).first()
        self.assertEqual(test_user_additional_info_data.user_id, response.json["user_id"])
        self.assertEqual(test_user_additional_info_data.is_organization_rep, response.json["is_organization_rep"])
        self.assertEqual(test_user_additional_info_data.timezone.value, response.json["timezone"])
        self.assertEqual(test_user_additional_info_data.additional_info["phone"], response.json["phone"])
        self.assertEqual(test_user_additional_info_data.additional_info["mobile"], response.json["mobile"])
        self.assertEqual(test_user_additional_info_data.additional_info["personal_website"], response.json["personal_website"])
        self.assertEqual(response.json, success_message)
        self.assertEqual(response.status_code, success_code)

        
        
    
    @patch("requests.get")
    def test_api_dao_get_non_existence_additional_info(self, mock_get_additional_info):
        error_message = messages.ADDITIONAL_INFORMATION_DOES_NOT_EXIST
        error_code = HTTPStatus.NOT_FOUND

        mock_response = Mock()
        mock_error = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_get_additional_info.return_value = mock_response
        mock_error.json.return_value = error_message
        mock_error.status_code = error_code
        mock_get_additional_info.side_effect = requests.exceptions.HTTPError(response=mock_error)

        with self.client:
            response = self.client.get(
                "/user/additional_info",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                follow_redirects=True,
                content_type="application/json",
            )
    
        test_user_additional_info_data = UserExtensionModel.query.filter_by(user_id=self.test_user_data.id).first()
        self.assertEqual(test_user_additional_info_data, None)
        self.assertEqual(response.json, error_message)
        self.assertEqual(response.status_code, error_code)
    

if __name__ == "__main__":
    unittest.main()
   