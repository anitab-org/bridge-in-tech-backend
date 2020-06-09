from http import HTTPStatus
# from typing import Dict
# from sqlalchemy import func
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app import messages


class UserExtensionDAO:
    
    """Data Access Object for Users_Extension functionalities"""

    @staticmethod
    def create_user_extension(data):
        """Creates a user_extension instance for a new registered user.

        Arguments:
            data: A list containing user's id, boolean value of whether or not
            the user is representing an organization, as well as their timezone
    
        Returns:
                A dictionary containing "message" which indicates whether or not the user_exension was created successfully and "code" for the HTTP response code.
        """

        user_id = data["user_id"]
        is_organization_rep = data["is_organization_rep"]
        timezone = data["timezone"]

        user_extension = UserExtensionModel(user_id, is_organization_rep, timezone)
        
        user_extension.save_to_db()

        response = {
            "message": f"{messages.USER_WAS_CREATED_SUCCESSFULLY}",
            "code": f"{HTTPStatus.CREATED}",
        }

        return response
