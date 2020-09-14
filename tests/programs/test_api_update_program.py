import unittest
from http import HTTPStatus, cookies
from unittest.mock import patch, Mock
from tests.base_test_case import BaseTestCase
from app import messages
from flask import json
from flask_restx import marshal
from app.api.models.user import full_user_api_model
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.api.request_api_utils import AUTH_COOKIE
from tests.test_data import user1, user2, program1, organization1
from app.database.models.bit_schema.program import ProgramModel


class TestUpdateProgramApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestUpdateProgramApi, self).setUp()
        # The access_expiry on this test is set to Wednesday, 30-Sep-20 15:03:56 UTC.
        # This date need to be adjusted accordingly once the development is near/pass the stated date
        # to make sure the test still pass.
        success_message = {"access_token": "this is fake token", "access_expiry": 1601478236}
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
        
        test_user1_data = UserModel.find_by_email(test_user1.email)
        AUTH_COOKIE["user"] = marshal(test_user1_data, full_user_api_model)

        test_user_extension = UserExtensionModel(
            user_id=test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user_extension.is_organization_rep = True
        test_user_extension.save_to_db()

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

        test_user_2_extension = UserExtensionModel(
            user_id=test_user2_data.id,
            timezone="EUROPE_KIEV"
        )
        test_user_2_extension.is_organization_rep = True
        test_user_2_extension.save_to_db()


        test_organization = OrganizationModel(
            rep_id=test_user1_data.id, 
            name="Company ABC",
            email="companyabc@mail.com",
            address="506 Elizabeth St, Melbourne VIC 3000, Australia",
            website="https://www.ames.net.au",
            timezone="AUSTRALIA_MELBOURNE",
        )

        test_organization.rep_department = "H&R Department"
        test_organization.about = "This is about ABC"
        test_organization.phone = "321-456-789"
        test_organization.status = "DRAFT"
        test_organization.join_date = 1601478236
        
        test_organization.save_to_db()
        
        self.test_organization_data = OrganizationModel.find_by_email(test_organization.email)

        test_organization_2 = OrganizationModel(
            rep_id=test_user2_data.id, 
            name="Company XYZ",
            email="companyxyz@mail.com",
            address="Singapore",
            website="",
            timezone="EUROPE_KIEV",
        )

        test_organization_2.rep_department = "H&R Department"
        test_organization_2.about = "This is about XYZ"
        test_organization_2.phone = "321-456-779"
        test_organization_2.status = "PUBLISH"
        test_organization_2.join_date = 1601478236
        
        test_organization_2.save_to_db()
        
        self.test_organization_2_data = OrganizationModel.find_by_email(test_organization_2.email)

        self.update_payload_program = {
            "program_name": "Program A",
            "start_date": "2020-10-15 23:00",
            "end_date": "2020-11-25 23:00",
            "organization_id": self.test_organization_data.id,
            "description": "Program A.",
            "target_skills": ["Java", "Ruby", "React"],
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
            "payment_amount": 4000,
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

        program1 = ProgramModel(
            program_name="Program A",
            start_date=1602763200,
            end_date=1606305600,
            organization_id=self.test_organization_data,
        )
        program1.description = "This is about Program A."
        program1.target_skills = ["Python", "Ruby", "React"]
        program1.target_candidate = {
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
        }
        program1.contact_type = "REMOTE"
        program1.zone = "GLOBAL"
        program1.status = "DRAFT"
        program1.creation_date = 1601424000
        program1.save_to_db()

        self.program_data_1 = ProgramModel.find_by_name("Program A")

        program2 = ProgramModel(
            program_name="Program B",
            start_date=1602343200,
            end_date=1602504500,
            organization_id=self.test_organization_2_data,
        )
        program2.description = "This is about Program B."
        program2.target_skills = ["C", "Lua"]
        program2.target_candidate = {
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
        }
        program2.contact_type = "REMOTE"
        program2.zone = "GLOBAL"
        program2.status = "CLOSED"
        program2.creation_date = 1601344000
        program2.save_to_db()

        self.program_data_2 = ProgramModel.find_by_name("Program B")


    def test_api_dao_update_program_successfully(self):
        # prepare existing program with 
        # start date 2020-10-15 12:00 GMT+0
        # and end date 2020-11-25 12:00 GMT+0

        response = self.client.put(
            f"/organizations/{self.test_organization_data.id}/programs/{self.program_data_1.id}",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                dict(self.update_payload_program)
                ),
            follow_redirects=True,
            content_type="application/json",
            )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(messages.PROGRAM_SUCCESSFULLY_UPDATED, response.json)

    def test_api_dao_update_program_with_invalid_organization(self):
        organization_id = 3

        response = self.client.put(
            f"/organizations/{organization_id}/programs/{self.program_data_1.id}",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                dict(self.update_payload_program)
                ),
            follow_redirects=True,
            content_type="application/json",
            )
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(messages.ORGANIZATION_DOES_NOT_EXIST, response.json)

    def test_api_dao_update_program_not_representative(self):
        response = self.client.put(
            f"/organizations/{self.test_organization_2_data.id}/programs/{self.program_data_2.id}",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                dict(self.update_payload_program)
                ),
            follow_redirects=True,
            content_type="application/json",
            )
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
        self.assertEqual(messages.USER_IS_NOT_THE_ORGANIZATION_REPRESENTATIVE, response.json)
