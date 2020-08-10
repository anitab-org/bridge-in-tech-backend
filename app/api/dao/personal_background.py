import ast
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
        
    @staticmethod
    def update_user_personal_background(data):
        """Creates or Updates a personal_background instance.

        Arguments:
            data: A list containing user's id, and user's background details (gender, 
            age, ethnicity, sexual_orientation, religion, physical_ability, mental_ability, 
            socio_economic, highest_education, years_of_experience, others) as well as 
            whether or not user agrees to make their personal background information
            public to other members of BridgeInTech.
    
        Returns:
                A dictionary containing "message" which indicates whether or not the user_exension 
                was created or updated successfully and "code" for the HTTP response code.
        """

        others_data = {}
        try:
            others_data["gender_other"] = data["gender_other"]
            others_data["ethnicity_other"] = data["ethnicity_other"]
            others_data["sexual_orientation_other"] = data["sexual_orientation_other"]
            others_data["religion_other"] = data["religion_other"]
            others_data["physical_ability_other"] = data["physical_ability_other"]
            others_data["mental_ability_other"] = data["mental_ability_other"]
            others_data["socio_economic_other"] = data["socio_economic_other"]
            others_data["highest_education_other"] = data["highest_education_other"]
        except KeyError as e:
            return e, HTTPStatus.BAD_REQUEST
        
        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        existing_personal_background = PersonalBackgroundModel.find_by_user_id(int(user["id"]))
        if not existing_personal_background:
            try:
                personal_background = PersonalBackgroundModel(
                    user_id=int(user["id"]),
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
                personal_background.others = others_data
                personal_background.is_public = data["is_public"]    
            except KeyError as e:
                return e, HTTPStatus.BAD_REQUEST

            personal_background.save_to_db()
            return messages.PERSONAL_BACKGROUND_SUCCESSFULLY_CREATED, HTTPStatus.CREATED
        
        try:
            existing_personal_background.gender = Gender(data["gender"]).name
            existing_personal_background.age = Age(data["age"]).name
            existing_personal_background.ethnicity = Ethnicity(data["ethnicity"]).name
            existing_personal_background.sexual_orientation = SexualOrientation(data["sexual_orientation"]).name
            existing_personal_background.religion = Religion(data["religion"]).name
            existing_personal_background.physical_ability = PhysicalAbility(data["physical_ability"]).name
            existing_personal_background.mental_ability = MentalAbility(data["mental_ability"]).name
            existing_personal_background.socio_economic = SocioEconomic(data["socio_economic"]).name
            existing_personal_background.highest_education = HighestEducation(data["highest_education"]).name
            existing_personal_background.years_of_experience = YearsOfExperience(data["years_of_experience"]).name
            existing_personal_background.is_public = data["is_public"]  
        except KeyError as e:
            return e, HTTPStatus.BAD_REQUEST

        existing_personal_background.others = others_data
        existing_personal_background.save_to_db()

        return messages.PERSONAL_BACKGROUND_SUCCESSFULLY_UPDATED, HTTPStatus.OK
