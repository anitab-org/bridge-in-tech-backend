import ast
import datetime
import logging
from http import HTTPStatus
import pytz
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.program import ProgramModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE, get_request, http_response_checker
from app.utils.bitschema_utils import *
from app.utils.bit_constants import MAX_PROGRAMS_PER_PAGE
from app.utils.date_converter import convert_human_date_to_timestamp, convert_timestamp_to_human_date


class ProgramDAO:
    
    """Data Access Object for Program functionalities"""

    @staticmethod
    def get_program_by_program_id(organization_id, program_id, token):
        """Retrieves a program which ID is passed as parameter.

        Arguments:
            organization_id: The ID of the organization where the program is offered.
            program_id: The ID of the program.
            token: The access token retrieved when login. 
            
        Returns:
            The ProgramModel class represented by its ID was searched.
        """
        
        organization = OrganizationModel.find_by_id(organization_id)
        if not organization:
            return messages.NO_ORGANIZATION_FOUND, HTTPStatus.NOT_FOUND
        user = http_response_checker(get_request("/users/"+f"{organization.rep_id}", token, params=None))
        if not user.status_code == 200:
            return user.message, user.status_code
        try:
            program = ProgramModel.find_by_id(program_id)
            if program.organization_id != organization_id:
                return messages.PROGRAM_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
        except AttributeError:
            return messages.PROGRAM_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
        return get_program(program, organization, user.message)

        
    @staticmethod
    def get_all_programs_by_organization(organization_id, token):

        """Retrieves all the programs that are offered by the organization which ID is passed as parameter.

        Arguments:
            organization_id: The ID of the organization where the program is offered.
            token: The access token retrieved when login. 
            
        Returns:
            The list of Programs offered by the orgranization which ID was searched.
        """

        organization = OrganizationModel.find_by_id(organization_id)
        if not organization:
            return messages.NO_ORGANIZATION_FOUND, HTTPStatus.NOT_FOUND
        user = http_response_checker(get_request("/users/"+f"{organization.rep_id}", token, params=None))
        if not user.status_code == 200:
            return user.message, user.status_code

        programs = ProgramModel.get_all_programs_by_organization(organization_id)
        if not programs:
            return messages.NO_PROGRAM_FOUND, HTTPStatus.NOT_FOUND
        return [get_program(program, organization, user.message) for program in programs]
        

    @staticmethod
    def create_program(organization_id, data):
        """Creates the program that is offered by organization which ID is passed as parameter.

        Arguments:
            organization_id: The ID of the organization which offer the program.
            data: The user input which contains the program details.

        Returns:
            A dictionary containing "message" which indicates whether or not 
            the program was created successfully and "code" for the HTTP response code.
        """

        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        representative_additional_info = UserExtensionModel.find_by_user_id(int(user["id"]))
        try:
            if representative_additional_info.is_organization_rep:
                try:
                    program_name = data["program_name"]
                    start_date = data["start_date"]
                    end_date = data["end_date"]
                except KeyError as e:
                    return e, HTTPStatus.BAD_REQUEST 

                organization = OrganizationModel.find_by_id(organization_id)
                if not organization:
                    return messages.ORGANIZATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
                if int(user["id"]) != organization.rep_id:
                    return messages.USER_IS_NOT_THE_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN

                timestamp_start_date = convert_human_date_to_timestamp(start_date, representative_additional_info.timezone.value)
                timestamp_end_date = convert_human_date_to_timestamp(end_date, representative_additional_info.timezone.value)
                program = ProgramModel(program_name, organization, timestamp_start_date, timestamp_end_date)
                return update(program, data, messages.PROGRAM_SUCCESSFULLY_CREATED, HTTPStatus.CREATED)  
        except AttributeError:
            return messages.NOT_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN

    @staticmethod
    def update_program(organization_id, program_id, data):
        """Updates the program that is offered by organization which 
        program and organization ID are passed as parameters.

        Arguments:
            organization_id: The ID of the organization which offer the program.
            program_id: The ID of the program.
            data: The user input which contains the program details.

        Returns:
            A dictionary containing "message" which indicates whether or not 
            the program was updated successfully and "code" for the HTTP response code.
        """

        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        representative_additional_info = UserExtensionModel.find_by_user_id(int(user["id"]))
        try:
            if representative_additional_info.is_organization_rep:
                try:
                    program_name = data["program_name"]
                    start_date = data["start_date"]
                    end_date = data["end_date"]
                except KeyError as e:
                    return e, HTTPStatus.BAD_REQUEST 

                organization = OrganizationModel.find_by_id(organization_id)
                if not organization:
                    return messages.ORGANIZATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
                if int(user["id"]) != organization.rep_id:
                    return messages.USER_IS_NOT_THE_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN
                program = ProgramModel.find_by_id(program_id)
                program.program_name = program_name
                
                timestamp_start_date = convert_human_date_to_timestamp(start_date, representative_additional_info.timezone.value)
                timestamp_end_date = convert_human_date_to_timestamp(end_date, representative_additional_info.timezone.value)
                program.start_date = timestamp_start_date
                program.end_date = timestamp_end_date
                return update(program, data, messages.PROGRAM_SUCCESSFULLY_UPDATED, HTTPStatus.OK)  
        except AttributeError:
            return messages.NOT_ORGANIZATION_REPRESENTATIVE, HTTPStatus.FORBIDDEN


def get_program(program, organization, user):
    try:
        user_json = (AUTH_COOKIE["user"].value)
        user = ast.literal_eval(user_json)
        representative_additional_info = UserExtensionModel.find_by_user_id(int(user["id"]))
        try:
            readable_start_date = convert_timestamp_to_human_date(program.start_date, representative_additional_info.timezone.value)
            readable_end_date = convert_timestamp_to_human_date(program.end_date, representative_additional_info.timezone.value)
            readable_creation_date = convert_timestamp_to_human_date(program.creation_date, representative_additional_info.timezone.value)
        except AttributeError:
            readable_start_date = convert_timestamp_to_human_date(program.start_date, Timezone.GMT0.value)
            readable_end_date = convert_timestamp_to_human_date(program.end_date, Timezone.GMT0.value)
            readable_creation_date = convert_timestamp_to_human_date(program.creation_date, Timezone.GMT0.value)

        return {
            "id":program.id,
            "program_name": program.program_name,
            "organization_id": program.organization_id,
            "organization_name": organization.name,
            "representative_id": user["id"],
            "representative_name": user["name"],
            "start_date": readable_start_date,  
            "end_date": readable_end_date,
            "description": program.description,
            "target_skills": program.target_skills,
            "target_candidate_gender": program.target_candidate["target_candidate_gender"],
            "target_candidate_age": program.target_candidate["target_candidate_age"],
            "target_candidate_ethnicity": program.target_candidate["target_candidate_ethnicity"],
            "target_candidate_sexual_orientation": program.target_candidate["target_candidate_sexual_orientation"],
            "target_candidate_religion": program.target_candidate["target_candidate_religion"],
            "target_candidate_physical_ability": program.target_candidate["target_candidate_physical_ability"],
            "target_candidate_mental_ability": program.target_candidate["target_candidate_mental_ability"],
            "target_candidate_socio_economic": program.target_candidate["target_candidate_socio_economic"],
            "target_candidate_highest_education": program.target_candidate["target_candidate_highest_education"],
            "target_candidate_years_of_experience": program.target_candidate["target_candidate_years_of_experience"],
            "target_candidate_other": program.target_candidate["target_candidate_other"],
            "payment_currency": program.payment_currency,
            "payment_amount": program.payment_amount,
            "contact_type": program.contact_type.value,
            "zone": program.zone.value,
            "student_responsibility": program.student_responsibility,
            "mentor_responsibility": program.mentor_responsibility,
            "organization_responsibility": program.organization_responsibility,
            "student_requirements": program.student_requirements,
            "mentor_requirements": program.mentor_requirements,
            "resources_provided": program.resources_provided,
            "contact_name": program.contact_name,
            "contact_department": program.contact_department,
            "program_address": program.program_address,
            "contact_phone": program.contact_phone,
            "contact_mobile": program.contact_mobile,
            "contact_email": program.contact_email,
            "program_website": program.program_website,
            "irc_channel": program.irc_channel,
            "tags": program.tags,
            "status": program.status.value,
            "creation_date":readable_creation_date
        }
    except TypeError as e:
        return e, HTTPStatus.BAD_REQUEST
        

def update(program, data, success_message, status_code):
    target_candidate_data = {}
    try:
        target_candidate_data["target_candidate_gender"] = data["target_candidate_gender"]
        target_candidate_data["target_candidate_age"] = data["target_candidate_age"]
        target_candidate_data["target_candidate_ethnicity"] = data["target_candidate_ethnicity"]
        target_candidate_data["target_candidate_sexual_orientation"] = data["target_candidate_sexual_orientation"]
        target_candidate_data["target_candidate_religion"] = data["target_candidate_religion"]
        target_candidate_data["target_candidate_physical_ability"] = data["target_candidate_physical_ability"]
        target_candidate_data["target_candidate_mental_ability"] = data["target_candidate_mental_ability"]
        target_candidate_data["target_candidate_socio_economic"] = data["target_candidate_socio_economic"]
        target_candidate_data["target_candidate_highest_education"] = data["target_candidate_highest_education"]
        target_candidate_data["target_candidate_years_of_experience"] = data["target_candidate_years_of_experience"]
        target_candidate_data["target_candidate_other"] = data["target_candidate_other"]
        program.description = data["description"]
        program.target_skills = data["target_skills"]
        program.target_candidate = target_candidate_data
        program.payment_currency = data["payment_currency"]
        program.payment_amount = data["payment_amount"]
        contact_type_value = data["contact_type"]
        program.contact_type = ContactType(contact_type_value).name
        zone_value = data["zone"]
        program.zone = Zone(zone_value).name
        program.student_responsibility = data["student_responsibility"]
        program.mentor_responsibility = data["mentor_responsibility"]
        program.organization_responsibility = data["organization_responsibility"]
        program.student_requirements = data["student_requirements"]
        program.mentor_requirements = data["mentor_requirements"]
        program.resources_provided = data["resources_provided"]
        program.contact_name = data["contact_name"]
        program.contact_department = data["contact_department"]
        program.program_address = data["program_address"]
        program.contact_phone = data["contact_phone"]
        program.contact_mobile = data["contact_mobile"]
        program.contact_email = data["contact_email"]
        program.program_website = data["program_website"]
        program.irc_channel = data["irc_channel"]
        program.tags = data["tags"]
        status_value = data["status"]
        program.status = ProgramStatus(status_value).name
    except KeyError as e:
        return e, HTTPStatus.BAD_REQUEST 

    program.save_to_db()

    return success_message, status_code 



