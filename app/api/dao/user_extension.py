from http import HTTPStatus
from flask import json
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE
from app.utils.bitschema_utils import Timezone


class UserExtensionDAO:
    
    """Data Access Object for Users_Extension functionalities"""

    @staticmethod
    def create_user_additional_info(data):
        """Creates a user_extension instance for a new registered user.

        Arguments:
            data: A list containing user's id, boolean value of whether or not
            the user is representing an organization, as well as their timezone
    
        Returns:
                A dictionary containing "message" which indicates whether or not the user_exension was created successfully and "code" for the HTTP response code.
        """

        try:
            user_id = AUTH_COOKIE["user_id"].value
        except KeyError:
            return messages.USER_ID_IS_NOT_RETRIEVED, HTTPStatus.FORBIDDEN
        
        timezone_value = data["timezone"]
            
        additional_info_data = {}
        
        existing_additional_info = UserExtensionModel.find_by_user_id(user_id)
        if existing_additional_info:
            return messages.ADDITIONAL_INFORMATION_OF_USER_ALREADY_EXIST, HTTPStatus.CONFLICT
        
        timezone = Timezone(timezone_value).name
        user_extension = UserExtensionModel(user_id, timezone)
        
        try:
            user_extension.is_organization_rep = data["is_organization_rep"]
            additional_info_data["phone"] = data["phone"]
            additional_info_data["mobile"] = data["mobile"]
            additional_info_data["personal_website"] = data["personal_website"]
        except KeyError as e:
            return e, HTTPStatus.BAD_REQUEST

        user_extension.additional_info = additional_info_data
        
        user_extension.save_to_db()

        return messages.ADDITIONAL_INFO_SUCCESSFULLY_CREATED, HTTPStatus.CREATED

    @staticmethod
    def get_user_additional_data_info(user_id):
        """Retrieves a user's additional information using a specified ID.

        Arguments:
            user_id: The ID of the user to be searched.

        Returns:
            The UserModel class of the user whose ID was searched, containing their additional information.
        """

        result = UserExtensionModel.find_by_user_id(user_id)
        if result:
            return {
                "user_id": result.user_id,
                "is_organization_rep": result.is_organization_rep,
                "timezone": result.timezone.value,
                "phone": result.additional_info["phone"],
                "mobile": result.additional_info["mobile"],
                "personal_website": result.additional_info["personal_website"]
            }
