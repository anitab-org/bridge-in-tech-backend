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
from app.api.request_api_utils import post_request, get_request, BASE_MS_API_URL, AUTH_COOKIE
from app.api.models.user import full_user_api_model, get_user_extension_response_model
from tests.test_data import user1
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel


class TestCreateUserAdditionalInfoApi(BaseTestCase):
    
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestCreateUserAdditionalInfoApi, self).setUp()
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

        AUTH_COOKIE["user"] = marshal(self.test_user_data, full_user_api_model)

        self.correct_payload_additional_info = {
            "is_organization_rep": True,
            "timezone": "Australia/Melbourne",
            "phone": "123-456-789",
            "mobile": "",
            "personal_website": ""
        }
        
    def test_api_dao_create_user_additional_info_successfully(self):
        success_message = messages.ADDITIONAL_INFO_SUCCESSFULLY_CREATED
        success_code = HTTPStatus.CREATED

        with self.client:
            response = self.client.put(
                "/user/additional_info",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                data=json.dumps(
                    dict(self.correct_payload_additional_info)
                ),
                follow_redirects=True,
                content_type="application/json",
            )

        test_user_additional_info_data = UserExtensionModel.query.filter_by(user_id=self.test_user_data.id).first()
        self.assertEqual(test_user_additional_info_data.user_id, self.test_user_data.id)
        self.assertEqual(test_user_additional_info_data.is_organization_rep, self.correct_payload_additional_info["is_organization_rep"])
        self.assertEqual(test_user_additional_info_data.timezone.value, self.correct_payload_additional_info["timezone"])
        self.assertEqual(test_user_additional_info_data.additional_info["phone"], self.correct_payload_additional_info["phone"])
        self.assertEqual(test_user_additional_info_data.additional_info["mobile"], self.correct_payload_additional_info["mobile"])
        self.assertEqual(test_user_additional_info_data.additional_info["personal_website"], self.correct_payload_additional_info["personal_website"])
        self.assertEqual(response.json, success_message)
        self.assertEqual(response.status_code, success_code)

    
    def test_api_dao_create_user_additional_info_invalid_payload(self):
        error_message = messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT
        error_code = HTTPStatus.BAD_REQUEST

        test_user_additional_info = {
            "is_organization_rep": True,
            "timezone": "Australia/Melbourne",
            "phone": "128abc",
            "mobile": "",
            "personal_website": ""
        }
        
        with self.client:
            response = self.client.put(
                "/user/additional_info",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                data=json.dumps(
                    dict(test_user_additional_info)
                ),
                follow_redirects=True,
                content_type="application/json",
            )

        test_user_additional_info_data = UserExtensionModel.query.filter_by(user_id=self.test_user_data.id).first()
        self.assertEqual(test_user_additional_info_data, None)
        self.assertEqual(response.json, error_message)
        self.assertEqual(response.status_code, error_code)

    
if __name__ == "__main__":
    unittest.main()
   