import logging
import ast
from http import HTTPStatus
from flask import json
from sqlalchemy import func
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE, get_request, http_response_checker
from app.utils.bitschema_utils import Timezone, OrganizationStatus
from app.utils.ms_constants import DEFAULT_PAGE, DEFAULT_USERS_PER_PAGE
from app.utils.bit_constants import MAX_ORGANIZATIONS_PER_PAGE
from app.utils.decorator_utils import http_response_namedtuple_converter
from app.utils.date_converter import convert_human_date_to_timestamp, convert_timestamp_to_human_date


class OrganizationDAO:
    
    """Data Access Object for Organization functionalities"""

    @staticmethod
    def get_organization(representative_id, representative_name):
        """Retrieves the organization that is represented by the user which ID is passed as parameter.

        Arguments:
            representative_id: The ID of the user who represents the organization.
        
        Returns:
            The OrganizationModel class represented by the user whose ID was searched.
        """

        return get_organization(representative_id, representative_name)
        

    @staticmethod
    def update_organization(data):
        """Creates or updates the organization that is represented by the user which ID is passed as parameter.

        Arguments:
            representative_id: The ID of the user who represents the organization.

        Returns:
            A dictionary containing "message" which indicates whether or not 
            the organization was created or updated successfully and "code" for the HTTP response code.
        """

        try:
            name = data["name"]
            email = data["email"]
            address = data["address"]
            website = data["website"]
            timezone_value = data["timezone"]
            timezone = Timezone(timezone_value).name  
        except KeyError as e:
            return e, HTTPStatus.BAD_REQUEST 

        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        representative_additional_info = UserExtensionModel.find_by_user_id(int(user["id"]))
        try:
            if representative_additional_info.is_organization_rep:
                organization = OrganizationModel.find_by_representative(int(user["id"]))
                if not organization:
                    organization = OrganizationModel(int(user["id"]), name, email, address, website, timezone)
                    return update(organization, data, messages.ORGANIZATION_SUCCESSFULLY_CREATED, HTTPStatus.CREATED)  
                organization.rep_id = int(user["id"])
                organization.name = name
                organization.email = email
                organization.address = address
                organization.website = website
                organization.timezone = timezone
                return update(organization, data, messages.ORGANIZATION_SUCCESSFULLY_UPDATED, HTTPStatus.OK)     
            return messages.NOT_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN
        except AttributeError:
            return messages.NOT_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN

    
    @staticmethod
    def list_organizations(
        name,
        page,
        per_page,
        token
    ):

        """ Retrieves a list of organizations with the specified ID.
        
        Arguments:
            user_id: The ID of the user to be listed.
            name: The search query for name of the organizations to be found.
            page: The page of organizations to be returned
            per_page: The number of organizations to return per page
        
        Returns:
            A list of organizations matching conditions and the HTTP response code.
        
        """

        organizations_list = (
            OrganizationModel.query.filter(func.lower(OrganizationModel.name).contains(name.lower())
            )
            .order_by(OrganizationModel.id)
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False,
                max_per_page=MAX_ORGANIZATIONS_PER_PAGE,
            )
            .items
        )
        list_of_organizations = [organization.json() for organization in organizations_list]
        user_params = {
            "search": "",
            "page": DEFAULT_PAGE,
            "per_page": DEFAULT_USERS_PER_PAGE
        }
        users = http_response_checker(get_request("/users/verified", token, params=user_params))
        if not users.status_code == 200:
            return users.message, users.status_code
        
        organizations_list = []
        try:
            for organization in list_of_organizations:
                if organization["status"].value == "Publish":
                    user_json = (AUTH_COOKIE["user"].value)
                    user = ast.literal_eval(user_json)  
                    if organization["rep_id"] == int(user['id']):
                        logged_in_user_organization = get_named_tuple_result(get_organization(int(user["id"]), user["name"]))
                        if logged_in_user_organization.status_code == 200:
                            organizations_list.append(logged_in_user_organization.message)
                    user_additional_info = UserExtensionModel.find_by_user_id(int(user["id"]))
                    for user in users.message:
                        member_additional_info = UserExtensionModel.find_by_user_id(user["id"])
                        try:
                            if member_additional_info.is_organization_rep:
                                if organization["rep_id"] == user["id"]:
                                    readable_join_date = ""
                                    try:
                                        readable_join_date = convert_timestamp_to_human_date(organization["join_date"], user_additional_info.timezone.value)
                                    except AttributeError:
                                            readable_join_date = convert_timestamp_to_human_date(organization["join_date"], Timezone.GMT0.value)
                                    organization_item = {
                                        "id": organization["id"],
                                        "representative_id": organization["rep_id"],
                                        "representative_name": user["name"],
                                        "representative_department": organization["rep_department"],
                                        "organization_name": organization["name"], 
                                        "email": organization["email"],
                                        "about": organization["about"],
                                        "address": organization["address"],
                                        "website": organization["website"],
                                        "timezone": organization["timezone"].value,
                                        "phone": organization["phone"],
                                        "status": organization["status"].value,
                                        "join_date": readable_join_date
                                    }
                                    organizations_list.append(organization_item)
                        except AttributeError as e:
                            logging.fatal(f"{e}")
            if not organizations_list:
                return messages.NO_ORGANIZATION_FOUND, HTTPStatus.NOT_FOUND
            return organizations_list, HTTPStatus.OK
        except ValueError:    
            return e, HTTPStatus.BAD_REQUEST


def update(organization, data, success_message, status_code):
    organization.rep_department = data["representative_department"]
    organization.about = data["about"]
    organization.phone = data["phone"]
    status_value = data["status"]
    organization.status = OrganizationStatus(status_value).name
    
    organization.save_to_db()

    return success_message, status_code 
        
        
def get_organization(user_id, user_name):
    representative_additional_info = UserExtensionModel.find_by_user_id(user_id)
    try:
        if representative_additional_info.is_organization_rep:
            readable_join_date = 0
            try:
                result = OrganizationModel.find_by_representative(user_id)
                readable_join_date = convert_timestamp_to_human_date(result.join_date, representative_additional_info.timezone.value)
                return {
                    "id": result.id,
                    "representative_id": result.rep_id,
                    "representative_name": user_name,
                    "representative_department": result.rep_department,
                    "organization_name":result.name, 
                    "email": result.email,
                    "about": result.about,
                    "address": result.address,
                    "website": result.website,
                    "timezone": result.timezone.value,
                    "phone": result.phone,
                    "status": result.status.value,
                    "join_date": readable_join_date
                }, HTTPStatus.OK
            except AttributeError:
                return messages.ORGANIZATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
    except AttributeError as e:
        logging.fatal(f"{e}")
    return messages.NOT_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN
    

@http_response_namedtuple_converter
def get_named_tuple_result(result):
    return result