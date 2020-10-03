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
from app.api.models.user import full_user_api_model
from app.api.models.organization import get_organization_response_model, update_organization_request_model
from tests.test_data import user1, user2, user3
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.api.models.user import public_user_personal_details_response_model
from app.utils.date_converter import convert_timestamp_to_human_date


class TestListOrganizationApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestListOrganizationApi, self).setUp()
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
        
        test_user2 = UserModel(
            name=user2["name"],
            username=user2["username"],
            password=user2["password"], 
            email=user2["email"], 
            terms_and_conditions_checked=user2["terms_and_conditions_checked"]
        )
        test_user2.need_mentoring = user2["need_mentoring"]
        test_user2.available_to_mentor = user2["available_to_mentor"]
        test_user2.is_email_verified = True

        test_user3 = UserModel(
            name=user3["name"],
            username=user3["username"],
            password=user3["password"], 
            email=user3["email"], 
            terms_and_conditions_checked=user3["terms_and_conditions_checked"]
        )
        test_user3.need_mentoring = user3["need_mentoring"]
        test_user3.available_to_mentor = user3["available_to_mentor"]
        test_user3.is_email_verified = True
        
        test_user2.save_to_db()
        test_user3.save_to_db()
        
        self.test_user2_data = UserModel.find_by_email(test_user2.email)
        self.test_user3_data = UserModel.find_by_email(test_user3.email)

        self.expected_users_list = [
            marshal(self.test_user2_data, public_user_personal_details_response_model),
            marshal(self.test_user3_data, public_user_personal_details_response_model)
        ]

        user1_extension = UserExtensionModel(
            user_id=self.test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        user1_extension.is_organization_rep = True
        
        user2_extension = UserExtensionModel(
            user_id=self.test_user2_data.id,
            timezone="ASIA_SINGAPORE"
        )
        user2_extension.is_organization_rep = True

        user3_extension = UserExtensionModel(
            user_id=self.test_user3_data.id,
            timezone="ASIA_SINGAPORE"
        )
        user3_extension.is_organization_rep = True
        
        user1_extension.save_to_db()
        user2_extension.save_to_db()
        user3_extension.save_to_db()
        
        
    @patch("requests.get")
    def test_api_dao_list_organization_successfully(self, mock_get_users):
        success_code = HTTPStatus.OK

        mock_get_response = Mock()
        mock_get_response.json.return_value = self.expected_users_list
        mock_get_response.status_code = success_code

        mock_get_users.return_value = mock_get_response
        mock_get_users.raise_for_status = json.dumps(success_code)

        organization1 = OrganizationModel(
            rep_id=self.test_user1_data.id, 
            name="Company ABC",
            email="companyabc@mail.com",
            address="506 Elizabeth St, Melbourne VIC 3000, Australia",
            website="https://www.ames.net.au",
            timezone="AUSTRALIA_MELBOURNE",
        )
        organization1.rep_department = "H&R Department"
        organization1.about = "This is about ABC"
        organization1.phone = "321-456-789"
        organization1.status = "PUBLISH"
        # joined one month prior to access date
        join_date = time.time() - 60*60*24*7
        organization1.join_date = join_date

        organization2 = OrganizationModel(
            rep_id=self.test_user2_data.id, 
            name="Company XYZ",
            email="companyxyz@mail.com",
            address="Singapore",
            website="",
            timezone="ASIA_SINGAPORE",
        )
        organization2.rep_department = "H&R Department"
        organization2.about = "This is about XYZ"
        organization2.phone = "321-456-789"
        organization2.status = "PUBLISH"
        organization2.join_date = join_date

        organization3 = OrganizationModel(
            rep_id=self.test_user3_data.id, 
            name="Company DEF",
            email="companydef@mail.com",
            address="Singapore",
            website="",
            timezone="ASIA_SINGAPORE",
        )
        organization3.rep_department = "H&R Department"
        organization3.about = "This is about DEF"
        organization3.phone = "321-456-789"
        organization3.status = "DRAFT"
        organization3.join_date = join_date

        organization1.save_to_db()
        organization2.save_to_db()
        organization3.save_to_db()

        organization1_data = OrganizationModel.find_by_representative(self.test_user1_data.id)
        organization2_data = OrganizationModel.find_by_representative(self.test_user2_data.id)
        organization3_data = OrganizationModel.find_by_representative(self.test_user3_data.id)
        
        expected_list_organizations = [
            {
                "id": organization1_data.id,
                "representative_id": self.test_user1_data.id,
                "representative_name": self.test_user1_data.name,
                "representative_department": "H&R Department",
                "organization_name": "Company ABC",
                "email": "companyabc@mail.com",
                "about": "This is about ABC",
                "address": "506 Elizabeth St, Melbourne VIC 3000, Australia",
                "website": "https://www.ames.net.au",
                "timezone": "Australia/Melbourne",
                "phone": "321-456-789",
                "status": "Publish",
                "join_date": convert_timestamp_to_human_date(join_date, "Australia/Melbourne"),
            },
            {
                "id": organization2_data.id,
                "representative_id": self.test_user2_data.id,
                "representative_name": self.test_user2_data.name,
                "representative_department": "H&R Department",
                "organization_name": "Company XYZ",
                "email": "companyxyz@mail.com",
                "about": "This is about XYZ",
                "address": "Singapore",
                "website": "",
                "timezone": "Asia/Singapore",
                "phone": "321-456-789",
                "status": "Publish",
                "join_date": convert_timestamp_to_human_date(join_date, "Australia/Melbourne"),
            }
        ]
        success_code = HTTPStatus.OK
        
        with self.client:
            list_organizations_response = self.client.get(
                "/organizations",
                headers={
                    "Authorization": AUTH_COOKIE["Authorization"].value,
                    "search": "",
                    "page": None,
                    "per_page": None,
                    "Accept": "application/json"
                }, 
                follow_redirects=True,
            )
        print(list_organizations_response.json)
        print(expected_list_organizations)
        self.assertEqual(list_organizations_response.json, expected_list_organizations)
        self.assertEqual(list_organizations_response.status_code, success_code)
        

    @patch("requests.get")
    def test_api_dao_get_organization_not_exist(self, mock_get_users):
        success_code = HTTPStatus.OK

        mock_get_response = Mock()
        mock_get_response.json.return_value = self.expected_users_list
        mock_get_response.status_code = success_code

        mock_get_users.return_value = mock_get_response
        mock_get_users.raise_for_status = json.dumps(success_code)
        
        with self.client:
            list_organizations_response = self.client.get(
                "/organizations",
                headers={
                    "Authorization": AUTH_COOKIE["Authorization"].value,
                    "search": "",
                    "page": None,
                    "per_page": None,
                    "Accept": "application/json"
                }, 
                follow_redirects=True,
            )
        self.assertEqual(HTTPStatus.NOT_FOUND, list_organizations_response.status_code)
        self.assertEqual(messages.NO_ORGANIZATION_FOUND, list_organizations_response.json)
