import ast
from http import HTTPStatus
from flask import json
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE
from app.utils.bitschema_utils import Timezone, OrganizationStatus


class OrganizationDAO:
    
    """Data Access Object for Users_Extension functionalities"""

    @staticmethod
    def get_organization(representative_id, representative_name):
        """Retrieves the organization that is represented by the user which ID is passed as parameter.

        Arguments:
            representative_id: The ID of the user who represents the organization.

        Returns:
            The OrganizationModel class represented by the user whose ID was searched.
        """

        representative_additional_info = UserExtensionModel.find_by_user_id(representative_id)
        try:
            if representative_additional_info.is_organization_rep:
                result = OrganizationModel.find_by_representative(representative_id)
                try:
                    return {
                        "representative_id": result.rep_id,
                        "representative_name": representative_name,
                        "representative_department": result.rep_department,
                        "organization_name":result.name, 
                        "email": result.email,
                        "about": result.about,
                        "address": result.address,
                        "website": result.website,
                        "timezone": result.timezone.value,
                        "phone": result.phone,
                        "status": result.status.value,
                        "join_date": result.join_date
                    }
                except AttributeError:
                    return messages.ORGANIZATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
        except AttributeError as e:
            logging.fatal(f"{e}")
        return messages.NOT_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN
    

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

def update(organization, data, success_message, status_code):
    organization.rep_department = data["representative_department"]
    organization.about = data["about"]
    organization.phone = data["phone"]
    status_value = data["status"]
    organization.status = OrganizationStatus(status_value).name
    
    organization.save_to_db()

    return success_message, status_code 
        
        
        