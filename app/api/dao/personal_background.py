from http import HTTPStatus
from flask import json
from app.database.models.bit_schema.personal_background import PersonalBackgroundModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE
from app.utils.bitschema_utils import *



class PersonalBackgroundDAO:
    
    """Data Access Object for Personal_Background functionalities"""

    @staticmethod
    def create_user_personal_background(data):
        """Creates a personal_background instance for a new registered user.

        Arguments:
            data: A list containing user's id, and user's background details (gender, 
            age, ethnicity, sexual_orientation, religion, physical_ability, mental_ability, 
            socio_economic, highest_education, years_of_experience, others) as well as 
            whether or not user agrees to make their personal background information
            public to other members of BridgeInTech.
    
        Returns:
                A dictionary containing "message" which indicates whether or not the user_exension 
                was created successfully and "code" for the HTTP response code.
        """

        user_id = int(AUTH_COOKIE["user_id"].value)
        if user_id == 0:    
            return messages.USER_ID_IS_NOT_RETRIEVED, HTTPStatus.FORBIDDEN
        existing_personal_background = PersonalBackgroundModel.find_by_user_id(user_id)
        if existing_personal_background:
            return messages.PERSONAL_BACKGROUND_OF_USER_ALREADY_EXIST, HTTPStatus.CONFLICT
        
        try:
            personal_background = PersonalBackgroundModel(
                user_id=user_id,
                gender=Gender(data["gender"]).name,
                age=Age(data["age"]).name,
                ethnicity=Ethnicity(data["ethnicity"]).name,
                sexual_orientation=SexualOrientation(data["sexual_orientation"]).name,
                religion=Religion(data["religion"]).name,
                physical_ability=PhysicalAbility(data["physical_ability"]).name,
                mental_ability=MentalAbility(data["mental_ability"]).name,
                socio_economic=SocioEconomic(data["socio_economic"]).name,
                highest_education=HighestEducation(data["highest_education"]).name,
                years_of_experience=YearsOfExperience(data["years_of_experience"]).name,
            )  
            personal_background.others = {
                "gender_other": data["gender_other"],
                "ethnicity_other": data["ethnicity_other"],
                "sexual_orientation_other": data["sexual_orientation_other"],
                "religion_other": data["religion_other"],
                "physical_ability_other": data["physical_ability_other"],
                "mental_ability_other": data["mental_ability_other"],
                "socio_economic_other": data["socio_economic_other"],
                "highest_education_other": data["highest_education_other"],
            } 
            personal_background.is_public = data["is_public"]    
        except KeyError as e:
            return e, HTTPStatus.BAD_REQUEST

        personal_background.save_to_db()

        return messages.PERSONAL_BACKGROUND_SUCCESSFULLY_CREATED, HTTPStatus.CREATED

    
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
        