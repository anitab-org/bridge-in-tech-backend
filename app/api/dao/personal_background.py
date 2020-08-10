from http import HTTPStatus
from flask import json
from app.database.models.bit_schema.personal_background import PersonalBackgroundModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE
from app.utils.bitschema_utils import *



class PersonalBackgroundDAO:
    
    """Data Access Object for Personal_Background functionalities"""

    @staticmethod
    def get_user_personal_background_info(user_id):
        """Retrieves a user's perrsonal background information using a specified ID.

        Arguments:
            user_id: The ID of the user to be searched.

        Returns:
            The PersonalBackgroundModel class of the user whose ID was searched, containing their additional information.
        """

        result = PersonalBackgroundModel.find_by_user_id(user_id)
        if result:
            return {
                "user_id": result.user_id,
                "gender": result.gender.value,
                "age": result.age.value,
                "ethnicity": result.ethnicity.value,
                "sexual_orientation": result.sexual_orientation.value,
                "religion": result.religion.value,
                "physical_ability": result.physical_ability.value,
                "mental_ability": result.mental_ability.value,
                "socio_economic": result.socio_economic.value,
                "highest_education": result.highest_education.value,
                "years_of_experience": result.years_of_experience.value,
                "gender_other": result.others["gender_other"],
                "ethnicity_other": result.others["ethnicity_other"],
                "sexual_orientation_other": result.others["sexual_orientation_other"],
                "religion_other": result.others["religion_other"],
                "physical_ability_other": result.others["physical_ability_other"],
                "mental_ability_other": result.others["mental_ability_other"],
                "socio_economic_other": result.others["socio_economic_other"],
                "highest_education_other": result.others["highest_education_other"],
                "is_public": result.is_public
            }
        