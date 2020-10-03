import time
import unittest
from http import HTTPStatus, cookies
from unittest.mock import patch, Mock
import requests
from requests.exceptions import HTTPError
from flask import json
from flask_restx import marshal
from app import messages
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from app.api.request_api_utils import post_request, get_request, BASE_MS_API_URL, AUTH_COOKIE
from app.api.models.user import full_user_api_model, public_user_personal_details_response_model
from app.api.models.organization import get_organization_response_model, update_organization_request_model
from tests.test_data import user1, user2
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.program import ProgramModel
from app.utils.date_converter import convert_timestamp_to_human_date


class TestCreateProgramApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestCreateProgramApi, self).setUp()
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
        AUTH_COOKIE["user"] = marshal(self.test_user1_data, full_user_api_model)

        test_user_extension = UserExtensionModel(
            user_id=self.test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user_extension.is_organization_rep = True
        test_user_extension.save_to_db()

        # prepare existing organization
        organization = OrganizationModel(
            rep_id=self.test_user1_data.id, 
            name="Company ABC",
            email="companyabc@mail.com",
            address="506 Elizabeth St, Melbourne VIC 3000, Australia",
            website="https://www.ames.net.au",
            timezone="AUSTRALIA_MELBOURNE",
        )
        organization.rep_department = "H&R Department"
        organization.about = "This is about ABC"
        organization.phone = "321-456-789"
        organization.status = "DRAFT"
        # joined one month prior to access date
        organization.join_date = time.time() - 60*60*24*7

        organization.save_to_db()
        self.organization1_data = OrganizationModel.find_by_representative(self.test_user1_data.id)
        
        # prepare expected representative object
        self.expected_representative = marshal(self.test_user1_data, public_user_personal_details_response_model)

        # set start date one month from now, end date another month after that
        start_date = time.time() + 60*60*24*28
        end_date = start_date + 60*60*24*28
        
        self.correct_payload_program = {
            "program_name": "Program A",
            "start_date": time.strftime("%Y-%m-%d %H:%M", time.localtime(start_date)),
            "end_date": time.strftime("%Y-%m-%d %H:%M", time.localtime(end_date)),
            "organization_id": self.organization1_data.id,
            "description": "This is about Program A.",
            "target_skills": ["Python", "Ruby", "React"],
            "target_candidate_gender": "Other",
            "target_candidate_age": "Not Applicable",
            "target_candidate_ethnicity": "Not Applicable",
            "target_candidate_sexual_orientation": "Not Applicable",
            "target_candidate_religion": "Not Applicable",
            "target_candidate_physical_ability": "Not Applicable",
            "target_candidate_mental_ability": "Not Applicable",
            "target_candidate_socio_economic": "Not Applicable",
            "target_candidate_highest_education": "Not Applicable",
            "target_candidate_years_of_experience": "Not Applicable",
            "target_candidate_other": "Non-Binary",
            "payment_currency": "USD",
            "payment_amount": 2000,
            "contact_type": "Remote",
            "zone": "Global",
            "student_responsibility": [],
            "mentor_responsibility": [],
            "organization_responsibility": [],
            "student_requirements": [],
            "mentor_requirements": [],
            "resources_provided": [],
            "contact_name": "Ms. Jane",
            "contact_department": "HRD",
            "program_address": "somewhere",
            "contact_phone": "123-432",
            "contact_mobile": "",
            "contact_email": "missjane@hrd.com",
            "program_website": "http://program_a.com",
            "irc_channel": "",
            "tags": [], 
            "status": "Draft"
        }
        
        
    @patch("requests.get")
    def test_api_dao_create_program_successfully(self, mock_get_representative):
        success_message = messages.PROGRAM_SUCCESSFULLY_CREATED
        success_code = HTTPStatus.CREATED

        mock_get_response = Mock()
        mock_get_response.json.return_value = self.expected_representative
        mock_get_response.status_code = success_code

        mock_get_representative.return_value = mock_get_response
        mock_get_representative.raise_for_status = json.dumps(success_code)

        response = self.client.post(
            f"/organizations/{self.organization1_data.id}/programs/program",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                    dict(self.correct_payload_program)
                ),
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(response.json, success_message)
        self.assertEqual(response.status_code, success_code)
        

    @patch("requests.get")
    def test_api_dao_create_program__but_not_representative(self, mock_get_representative):
        # create another user representative
        test_user2 = UserModel(
            name=user2["name"],
            username=user2["username"],
            password=user2["password"], 
            email=user2["email"], 
            terms_and_conditions_checked=user2["terms_and_conditions_checked"]
        )
        test_user2.need_mentoring = user2["need_mentoring"]
        test_user2.available_to_mentor = user2["available_to_mentor"]

        test_user2.save_to_db()
        test_user2_data = UserModel.find_by_email(test_user2.email)

        # create another orgnazation
        organization2 = OrganizationModel(
            rep_id=test_user2_data.id, 
            name="Company DEF",
            email="companydef@mail.com",
            address="Somewhere",
            website="https://www.def.net",
            timezone="PACIFIC_POHNPEI",
        )
        organization2.rep_department = "H&R Department"
        organization2.about = "This is about DEF"
        organization2.phone = "321-456-789"
        organization2.status = "DRAFT"
        organization2.join_date = time.time() - 60*60*24*7

        organization2.save_to_db()
        organization2_data = OrganizationModel.find_by_representative(test_user2_data.id)

        mock_get_response = Mock()
        mock_get_response.json.return_value = self.expected_representative
        mock_get_response.status_code = HTTPStatus.OK

        mock_get_representative.return_value = mock_get_response
        mock_get_representative.raise_for_status = json.dumps(HTTPStatus.OK)
        

        response = self.client.post(
            f"/organizations/{organization2_data.id}/programs/program",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                    dict(self.correct_payload_program)
                ),
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
        self.assertEqual(messages.USER_IS_NOT_THE_ORGANIZATION_REPRESENTATIVE, response.json)

    
    @patch("requests.get")
    def test_api_dao_create_program_but_organization_not_exist(self, mock_get_representative):
        mock_get_response = Mock()
        mock_get_response.json.return_value = self.expected_representative
        mock_get_response.status_code = HTTPStatus.OK

        mock_get_representative.return_value = mock_get_response
        mock_get_representative.raise_for_status = json.dumps(HTTPStatus.OK)
        
        response = self.client.post(
            "/organizations/3/programs/program",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                    dict(self.correct_payload_program)
                ),
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(messages.ORGANIZATION_DOES_NOT_EXIST, response.json)
