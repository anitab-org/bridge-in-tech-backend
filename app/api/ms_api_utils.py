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
    
def http_response_checker(result, request_type):
    
    if result[1] == HTTPStatus.OK:
        return http_ok_status_checker(result, request_type)
    if result[1] == HTTPStatus.BAD_REQUEST:
        return http_bad_request_checker(result)
    
    # TO DO. CHANGE HTTPStatus.NOT_FOUND to UNAUTHORIZED AFTER PR647 IN MS BACKEND IS APPROVED
    if request_type == "login":
        if result[1] == HTTPStatus.NOT_FOUND:
            return messages.WRONG_USERNAME_OR_PASSWORD, HTTPStatus.UNAUTHORIZED
    
    if result[1] == HTTPStatus.FORBIDDEN:
        return messages.USER_HAS_NOT_VERIFIED_EMAIL_BEFORE_LOGIN, HTTPStatus.FORBIDDEN
    if result[1] == HTTPStatus.INTERNAL_SERVER_ERROR:
        return messages.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR
    # for all other errors
    return result
    
def http_bad_request_checker(result):
    
    if result[0] == f"{messages.USERNAME_FIELD_IS_MISSING}":
        return messages.USERNAME_FIELD_IS_MISSING, HTTPStatus.BAD_REQUEST
    if result[0] == f"{messages.PASSWORD_FIELD_IS_MISSING}":
        return messages.PASSWORD_FIELD_IS_MISSING, HTTPStatus.BAD_REQUEST
    
def http_ok_status_checker(result, request_type):
    if result[1] == HTTPStatus.OK:
        if request_type == "register":
            return messages.USER_WAS_CREATED_SUCCESSFULLY, HTTPStatus.CREATED
        if request_type == "login":
            result_to_show = {
                "access_token": result[0].get("access_token"),
                "access_expiry": result[0].get("access_expiry"),
            }
            return result_to_show, HTTPStatus.OK
    
