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
from app.api.models.user import full_user_api_model, get_user_personal_background_response_model
from tests.test_data import user1
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.personal_background import PersonalBackgroundModel


class TestCreatePersonalBackgroundApi(BaseTestCase):
    
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestCreatePersonalBackgroundApi, self).setUp()
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
        self.correct_payload_personal_background = {
            "gender": "Female",
            "age": "Between 55 to 64 yo",
            "ethnicity": "Middle Eastern/North African (MENA)",
            "sexual_orientation": "Prefer not to say",
            "religion": "Islam",
            "physical_ability": "With/had limited physical ability (or with/had some type of physical disability/ies)",
            "mental_ability": "With/previously had some type of mental disorders",
            "socio_economic": "Lower Middle class (e.g. blue collars in skilled trades/Paralegals/Bank tellers/Sales/Clerical-Admin/other support workers)",
            "highest_education": "Prefer not to say",
            "years_of_experience": "Prefer not to say",
            "gender_other": "They",
            "ethnicity_other": "",
            "sexual_orientation_other": "",
            "religion_other": "Daoism",
            "physical_ability_other": "",
            "mental_ability_other": "",
            "socio_economic_other": "",
            "highest_education_other": "",
            "is_public": False
        }
        
        
    def test_api_dao_create_user_personal_background_successfully(self):
        success_message = messages.PERSONAL_BACKGROUND_SUCCESSFULLY_CREATED
        success_code = HTTPStatus.CREATED

        with self.client:
            response = self.client.put(
                "/user/personal_background",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                data=json.dumps(
                    dict(self.correct_payload_personal_background)
                ),
                follow_redirects=True,
                content_type="application/json",
            )

        test_user_personal_background_data = PersonalBackgroundModel.query.filter_by(user_id=self.test_user_data.id).first()
        self.assertEqual(test_user_personal_background_data.user_id, self.test_user_data.id)
        self.assertEqual(test_user_personal_background_data.gender.value, self.correct_payload_personal_background["gender"])
        self.assertEqual(test_user_personal_background_data.age.value, self.correct_payload_personal_background["age"])
        self.assertEqual(test_user_personal_background_data.ethnicity.value, self.correct_payload_personal_background["ethnicity"])
        self.assertEqual(test_user_personal_background_data.sexual_orientation.value, self.correct_payload_personal_background["sexual_orientation"])
        self.assertEqual(test_user_personal_background_data.religion.value, self.correct_payload_personal_background["religion"])
        self.assertEqual(test_user_personal_background_data.physical_ability.value, self.correct_payload_personal_background["physical_ability"])
        self.assertEqual(test_user_personal_background_data.mental_ability.value, self.correct_payload_personal_background["mental_ability"])
        self.assertEqual(test_user_personal_background_data.socio_economic.value, self.correct_payload_personal_background["socio_economic"])
        self.assertEqual(test_user_personal_background_data.highest_education.value, self.correct_payload_personal_background["highest_education"])
        self.assertEqual(test_user_personal_background_data.years_of_experience.value, self.correct_payload_personal_background["years_of_experience"])
        self.assertEqual(test_user_personal_background_data.others["gender_other"], self.correct_payload_personal_background["gender_other"])
        self.assertEqual(test_user_personal_background_data.others["ethnicity_other"], self.correct_payload_personal_background["ethnicity_other"])
        self.assertEqual(test_user_personal_background_data.others["sexual_orientation_other"], self.correct_payload_personal_background["sexual_orientation_other"])
        self.assertEqual(test_user_personal_background_data.others["religion_other"], self.correct_payload_personal_background["religion_other"])
        self.assertEqual(test_user_personal_background_data.others["physical_ability_other"], self.correct_payload_personal_background["physical_ability_other"])
        self.assertEqual(test_user_personal_background_data.others["mental_ability_other"], self.correct_payload_personal_background["mental_ability_other"])
        self.assertEqual(test_user_personal_background_data.others["socio_economic_other"], self.correct_payload_personal_background["socio_economic_other"])
        self.assertEqual(test_user_personal_background_data.others["highest_education_other"], self.correct_payload_personal_background["highest_education_other"])
        self.assertEqual(test_user_personal_background_data.is_public, self.correct_payload_personal_background["is_public"])
        self.assertEqual(response.json, success_message)
        self.assertEqual(response.status_code, success_code)

    
    def test_api_dao_create_user_personal_background_invalid_payload(self):
        error_message = messages.PERSONAL_BACKGROUND_IS_INVALID
        error_code = HTTPStatus.BAD_REQUEST

        test_user_personal_background = {
            "gender": "Some random value",
            "age": "Between 55 to 64 yo",
            "ethnicity": "Middle Eastern/North African (MENA)",
            "sexual_orientation": "Prefer not to say",
            "religion": "Islam",
            "physical_ability": "With/had limited physical ability (or with/had some type of physical disability/ies)",
            "mental_ability": "With/previously had some type of mental disorders",
            "socio_economic": "Lower Middle class (e.g. blue collars in skilled trades/Paralegals/Bank tellers/Sales/Clerical-Admin/other support workers)",
            "highest_education": "Prefer not to say",
            "years_of_experience": "Prefer not to say",
            "gender_other": "They",
            "ethnicity_other": "",
            "sexual_orientation_other": "",
            "religion_other": "Daoism",
            "physical_ability_other": "",
            "mental_ability_other": "",
            "socio_economic_other": "",
            "highest_education_other": "",
            "is_public": False
        }
        
        with self.client:
            response = self.client.put(
                "/user/personal_background",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                data=json.dumps(
                    dict(test_user_personal_background)
                ),
                follow_redirects=True,
                content_type="application/json",
            )

        test_user_personal_background_data = PersonalBackgroundModel.query.filter_by(user_id=self.test_user_data.id).first()
        self.assertEqual(test_user_personal_background_data, None)
        self.assertEqual(response.json, error_message)
        self.assertEqual(response.status_code, error_code)

    
if __name__ == "__main__":
    unittest.main()

   