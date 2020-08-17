import ast
from http import HTTPStatus
from flask import json
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE
from app.utils.bitschema_utils import Timezone


class UserExtensionDAO:
    
    """Data Access Object for Users_Extension functionalities"""

    @staticmethod
    def get_user_additional_data_info(user_id):
        """Retrieves a user's additional information using a specified ID.

        Arguments:
            user_id: The ID of the user to be searched.

        Returns:
            The UserExtensionModel class of the user whose ID was searched, containing their additional information.
        """

        result = UserExtensionModel.find_by_user_id(user_id)
        if result:
            try:
                phone = result.additional_info["phone"]
                mobile = result.additional_info["mobile"]
                personal_website = result.additional_info["personal_website"]
                return {
                    "user_id": result.user_id,
                    "is_organization_rep": result.is_organization_rep,
                    "timezone": result.timezone.value,
                    "phone": phone,
                    "mobile": mobile,
                    "personal_website": personal_website
                }
            except TypeError:
                return {
                    "user_id": result.user_id,
                    "is_organization_rep": result.is_organization_rep,
                    "timezone": result.timezone.value,
                    "phone": "",
                    "mobile": "",
                    "personal_website": ""
                }
        return

    @staticmethod
    def update_user_additional_info(data):
        """Updates a user_extension instance.
        Arguments:
        data: A list containing user's id, boolean value of whether or not
        the user is representing an organization, as well as their timezone
        Returns:
                A dictionary containing "message" which indicates whether or not 
                the user_exension was updated successfully and "code" for the HTTP response code.
        """

        timezone_value = data["timezone"]
        timezone = Timezone(timezone_value).name   

        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        user_additional_info = UserExtensionModel.find_by_user_id(int(user["id"]))
        if not user_additional_info:
            user_additional_info = UserExtensionModel(int(user["id"]), timezone)
            return update(user_additional_info, data, timezone, messages.ADDITIONAL_INFO_SUCCESSFULLY_CREATED, HTTPStatus.CREATED)    
        return update(user_additional_info, data, timezone, messages.ADDITIONAL_INFO_SUCCESSFULLY_UPDATED, HTTPStatus.OK)     
    
def update(user, data, timezone, success_message, status_code):
    additional_info_data = {}
    try:
        additional_info_data["phone"] = data["phone"]
        additional_info_data["mobile"] = data["mobile"]
        additional_info_data["personal_website"] = data["personal_website"]
        user.is_organization_rep = data["is_organization_rep"]
    except KeyError as e:
        return e, HTTPStatus.BAD_REQUEST

    user.timezone = timezone
    user.additional_info = additional_info_data
    user.save_to_db()

    return success_message, status_code 
