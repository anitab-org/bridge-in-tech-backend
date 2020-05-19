from app.database.sqlalchemy_extension import db
    
from app.database.models.ms_schema.user import UserModel
from app.database.models.ms_schema.mentorship_relation import MentorshipRelationModel
from app.database.models.ms_schema.tasks_list import TasksListModel
from app.database.models.ms_schema.task_comment import TaskCommentModel
from app.database.models.bit_schema.organization import OrganizationModel
from app.database.models.bit_schema.program import ProgramModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.database.models.bit_schema.personal_background import PersonalBackgroundModel
from app.database.models.bit_schema.mentorship_relation_extension import MentorshipRelationExtensionModel
import requests
from requests.exceptions import HTTPError

def query_mock_data():
    # set base url

    # for ms-api local server
    base_ms_api_url = "http://127.0.0.1:4000"

    # for ms-api heroku server
    # base_ms_api_url = "https://mentorship-backend-temp.herokuapp.com"

    # register user
    try:
        response = requests.post(
            f"{base_ms_api_url}/register",
            json = {
                "name": "mttest",
                "username": "mttest01",
                "password": "mttest01",
                "email": "cejela2101@provlst.com",
                'terms_and_conditions_checked': True,
                "need_mentoring": True,
                "available_to_mentor": False
            },
            headers = {"Accept": "application/json"}
        )
    except HTTPError as http_err:
        print(f"HTTP error occoured: {http_err}")
    except Exception as err:
        print(f"Other error occured: {err}")
    else:
        response.encoding = "utf-8"
        body = response.text
        json_response = response.json()
        print(f"{body}")
        print(f"{json_response}")