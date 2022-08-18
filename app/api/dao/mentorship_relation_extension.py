import ast
from http import HTTPStatus
from flask import json
from app.database.models.bit_schema.mentorship_relation_extension import  MentorshipRelationExtensionModel
from app import messages
from app.api.request_api_utils import AUTH_COOKIE
from app.utils.bitschema_utils import Timezone


class MentorshipRelationExtensionDAO:
    
    """Data Access Object for Users_Extension functionalities"""

    @staticmethod
    def createMentorshipRelationExtension(program_id, mentorship_relation_id , mentee_request_date):
        """Creates the extending mentorship relation between organization's program and the user which is logged in.

        Arguments:
            organization_id: The ID organization
            program_id: The ID of program

        Returns:
            A dictionary containing "message" which indicates whether or not 
            the relation was created successfully and "code" for the HTTP response code.
        """        
        
        try:
            mentorship_relation_extension_object =  MentorshipRelationExtensionModel(program_id,mentorship_relation_id)
            mentorship_relation_extension_object.mentee_request_date = mentee_request_date
            mentorship_relation_extension_object.save_to_db()
            return messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, HTTPStatus.CREATED 
        except:
            return messages.INTERNAL_SERVER_ERROR, HTTPStatus.BAD_REQUEST

        
              
    