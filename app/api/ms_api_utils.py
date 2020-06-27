import logging
from http import HTTPStatus
from flask import json
import requests
from app import messages


# set base url

# for ms-api local server
BASE_MS_API_URL = "http://127.0.0.1:4000"

# for MS-API on Heroku server
# WARNING!!! When you push a PR, for travis to pass test cases related to MS API
# Heroku MS API needs to be set as preference over the localhost. Otherwise, make sure
# you run the MS API local server when you push the PR.
# BASE_MS_API_URL = "https://bridge-in-tech-ms-test.herokuapp.com"


# create instance
def post_request(request_url, data):
    
    try:
        response = requests.post(
            request_url, json=data, headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        response_message = response.json()
        response_code = response.status_code
    except requests.exceptions.ConnectionError as e:
        response_message = messages.INTERNAL_SERVER_ERROR
        response_code = json.dumps(HTTPStatus.INTERNAL_SERVER_ERROR)
        logging.fatal(f"{e}")
    except requests.exceptions.HTTPError as e:
        response_message = e.response.json()
        response_code = e.response.status_code
    except Exception as e:
        response_message = messages.INTERNAL_SERVER_ERROR
        response_code = json.dumps(HTTPStatus.INTERNAL_SERVER_ERROR)
        logging.fatal(f"{e}")
    finally:
        logging.fatal(f"{response_message}")
        return response_message, response_code
        