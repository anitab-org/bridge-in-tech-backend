import logging
import requests
from http import HTTPStatus
from app import messages

# from requests.exceptions import HTTPError
from flask import json
# from urllib3.exceptions import HTTPError
# from werkzeug.exceptions import HTTPException

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
    except requests.ConnectionError as e:
        return f"{e.response.json()}", HTTPStatus.INTERNAL_SERVER_ERROR
    except requests.HTTPError as e:
        return f"{e.response.json()}", e.response.status_code
    except Exception as e:
        return f"{e.response.json()}", e.response.status_code
    else:
        logging.warning(f"{response}")
        return f"{response.json()}", response.status_code
