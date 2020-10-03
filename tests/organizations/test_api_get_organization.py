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
from tests.test_data import user1
from app.database.models.ms_schema.user import UserModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.utils.date_converter import convert_timestamp_to_human_date


class TestGetOrganizationApi(BaseTestCase):
    @patch("requests.get")
    @patch("requests.post")
    def setUp(self, mock_login, mock_get_user):
        super(TestGetOrganizationApi, self).setUp()
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
        
        
    def test_api_dao_get_organization_successfully(self):
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
        join_date = time.time() - 60*60*24*7
        organization.join_date = join_date

        db.session.add(organization)
        db.session.commit()

        organization1_data = OrganizationModel.find_by_representative(self.test_user1_data.id)
        
        test_user_extension = UserExtensionModel(
            user_id=self.test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user_extension.is_organization_rep = True
        test_user_extension.save_to_db()

        response_organization = {
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
            "status": "Draft",
            "join_date": convert_timestamp_to_human_date(join_date, "Australia/Melbourne"),
        }
        success_code = HTTPStatus.OK
        
        response = self.client.get(
            "/organization",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(response.json, response_organization)
        self.assertEqual(response.status_code, success_code)
        

    def test_api_dao_get_organization_not_exist(self):
        test_user_extension = UserExtensionModel(
            user_id=self.test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user_extension.is_organization_rep = True
        test_user_extension.save_to_db()
        
        response = self.client.get(
            "/organization",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(messages.ORGANIZATION_DOES_NOT_EXIST, response.json)

    
    def test_api_dao_get_organization_not_representative(self):
        test_user_extension = UserExtensionModel(
            user_id=self.test_user1_data.id,
            timezone="AUSTRALIA_MELBOURNE"
        )
        test_user_extension.is_organization_rep = False
        test_user_extension.save_to_db()

        response = self.client.get(
            "/organization",
            headers={"Authorization": AUTH_COOKIE["Authorization"].value},
            follow_redirects=True,
            content_type="application/json",
        )
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
        self.assertEqual(messages.NOT_ORGANIZATION_REPRESENTATIVE, response.json)