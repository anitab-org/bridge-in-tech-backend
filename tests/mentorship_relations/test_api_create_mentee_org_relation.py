import time
import unittest
from unittest.mock import patch, Mock
from http import HTTPStatus, cookies
import requests
from requests.exceptions import HTTPError
# Flask
from flask import json
from flask_restx import marshal
# app
from app import messages
from app.database.sqlalchemy_extension import db
# Api Models
from app.api.models.user import full_user_api_model, public_user_personal_details_response_model
from app.api.models.organization import get_organization_response_model, update_organization_request_model
from app.api.models.mentorship_relation import send_mentorship_extension_request_body 
# Test
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2
# Utils
from app.utils.date_converter import convert_timestamp_to_human_date
from app.api.request_api_utils import post_request, get_request, BASE_MS_API_URL, AUTH_COOKIE
# Database model
## ms schema
from app.database.models.ms_schema.user import UserModel
from app.database.models.ms_schema.mentorship_relation import MentorshipRelationModel
from app.database.models.ms_schema.tasks_list import TasksListModel
## bit schema
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.program import ProgramModel
from app.database.models.bit_schema.mentorship_relation_extension import MentorshipRelationExtensionModel

class TestCreateMenteeOrgRelationByOrgApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestCreateMenteeOrgRelationByOrgApi, self).setUp()
        # set access expiry 4 weeks from today's date (sc*min*hrrs*days)
        access_expiry = time.time() + 60*60*24*28
        success_message = {"access_token": "this is fake token", "access_expiry": access_expiry}
        success_code = HTTPStatus.OK

        # Mocking Login
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
        
        # Creating test_user1 
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

        # Extending test_user1
        test_user1_extension = UserExtensionModel(
            user_id=self.test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user1_extension.is_organization_rep = True
        test_user1_extension.save_to_db()

        # preparing organization
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
        self.organization_data = OrganizationModel.find_by_representative(self.test_user1_data.id)
        
        # prepare expected representative object
        self.expected_representative = marshal(self.test_user1_data, public_user_personal_details_response_model)

        # set start date one month from now, end date another month after that
        start_date = time.time() + 60*60*24*28
        end_date = start_date + 60*60*24*28
        creation_date = start_date - 60*60*24*14
        program = ProgramModel(
            program_name="Program A",
            start_date=start_date,
            end_date=end_date,
            organization_id=self.organization_data,
        )
        program.description = "This is about Program A."
        program.target_skills = ["Python", "Ruby", "React"]
        program.target_candidate = {
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
        program.contact_type = "REMOTE"
        program.zone = "GLOBAL"
        program.status = "DRAFT"
        program.creation_date = creation_date
        program.save_to_db()
        
        self.program_data = ProgramModel.find_by_name("Program A")

        # mentee user 
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
        self.test_user2_data = UserModel.find_by_email(test_user2.email)
        
        test_user2_extension = UserExtensionModel(
            user_id=self.test_user2_data .id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user2_extension.is_organization_rep = True
        test_user2_extension.save_to_db()

        self.correct_mentee_org_relation_body = {
            "mentee_id": self.test_user2_data.id,
            "mentee_request_date": time.time() + 60*60*24*7,
            "end_date": time.time() + 2*60*60*24*7,
            "notes": "Please Add"
        }

    @patch("requests.post")
    def test_api_dao_create_mentee_org_relation_successfully(self,mock_create_org_mentee_relation):
        
        success_message = messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY
        success_code = HTTPStatus.BAD_REQUEST
        
        mock_response = Mock()
        mock_response.json.return_value = success_message
        mock_response.status_code = success_code
        mock_create_org_mentee_relation.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_create_org_mentee_relation.return_value = mock_response
        mock_create_org_mentee_relation.raise_for_status = json.dumps(success_code)

        with self.client:
            response = self.client.post(
                f"/organizations/{self.organization_data.id}/programs/{self.program_data.id}/send_request",
                headers={"Authorization": AUTH_COOKIE["Authorization"].value},
                data=json.dumps(
                    dict(self.correct_mentee_org_relation_body)
                ),
                follow_redirects=True,
                content_type="application/json",
            )

        tasks_list = TasksListModel()
        tasks_list.save_to_db()
        
        test_org_mentee_relation = MentorshipRelationModel(
            action_user_id = self.test_user1_data.id,
            mentor_user = self.test_user1_data,
            mentee_user = self.test_user2_data,
            creation_date = time.time(),
            end_date = self.correct_mentee_org_relation_body['end_date'],
            state = 'PENDING',
            notes = self.correct_mentee_org_relation_body['notes'],
            tasks_list = tasks_list
        )
        test_org_mentee_relation.save_to_db()
        test_org_mentee_relation_data = MentorshipRelationModel.find_by_id(test_org_mentee_relation.id)
        test_org_mentee_relation_extension = MentorshipRelationExtensionModel(self.program_data.id,test_org_mentee_relation_data.id)
        test_org_mentee_relation_extension_data = MentorshipRelationExtensionModel.find_by_id(test_org_mentee_relation_extension.id)
        
        mock_create_org_mentee_relation.assert_called()        
        self.assertEqual(success_code, response.status_code)
        self.assertEqual(response.json,success_message)
    

    def test_api_dao_create_mentee_org_relation_invalid_program(self):

        invalid_program_id = 20
        response = self.client.post(
            f"/organizations/{self.organization_data.id}/programs/{invalid_program_id}/send_request",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                dict(self.correct_mentee_org_relation_body)
                ),
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(messages.PROGRAM_DOES_NOT_EXIST , response.json)
    
    @patch("requests.post")
    def test_api_dao_create_mentee_org_relation_mentee_not_found(self,mock_create_org_mentee_relation):
        
        error_message = messages.MENTEE_DOES_NOT_EXIST
        error_code = HTTPStatus.BAD_REQUEST
        
        mock_response = Mock()
        mock_response.json.return_value = error_message
        mock_response.status_code = error_code
        mock_create_org_mentee_relation.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_create_org_mentee_relation.return_value = mock_response
        mock_create_org_mentee_relation.raise_for_status = json.dumps(error_code)

        incorrect_mentee_org_relation_body = {
            "mentee_id": 200,
            "mentee_request_date": time.time() + 60*60*24*7,
            "end_date": time.time() + 2*60*60*24*7,
            "notes": "Please Add"
        }

        response = self.client.post(
            f"/organizations/{self.organization_data.id}/programs/{self.program_data.id}/send_request",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            data=json.dumps(
                dict(incorrect_mentee_org_relation_body)
                ),
            follow_redirects=True,
            content_type="application/json",
        )

        self.assertEqual(error_code, response.status_code)
        self.assertEqual(error_message, response.json)


