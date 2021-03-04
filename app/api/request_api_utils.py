import logging
from http import HTTPStatus, cookies
from datetime import datetime
from flask import json
import requests
from app import messages
from app.utils.decorator_utils import http_response_namedtuple_converter


BASE_MS_API_URL = "http://127.0.0.1:4000"
AUTH_COOKIE = cookies.SimpleCookie()


def post_request(request_string, data):
    request_url = f"{BASE_MS_API_URL}{request_string}" 
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
        if request_string == "/login" and response_code == HTTPStatus.OK:
            access_token_cookie = response_message.get("access_token")
            access_expiry_cookie = response_message.get("access_expiry")
            AUTH_COOKIE["Authorization"] = f"Bearer {access_token_cookie}"
            AUTH_COOKIE["Authorization"]["expires"] = access_expiry_cookie
            set_user = http_response_checker(get_user(AUTH_COOKIE["Authorization"].value))
            if set_user.status_code != 200:
                response_message = set_user.message
                response_code = set_user.status_code
            else:
                response_message = {"access_token": response_message.get("access_token"), "access_expiry": response_message.get("access_expiry")}
        logging.fatal(f"{response_message}")
        return response_message, response_code


def get_user(token):
    request_url = "/user" 
    return get_request(request_url, token, params=None)


def get_headers(request_string, params):
    if request_string == "/user":
        return {"Authorization": AUTH_COOKIE["Authorization"].value, "Accept": "application/json"}
    if request_string == "/users/verified":
        return {
            "Authorization": AUTH_COOKIE["Authorization"].value, 
            "search": params["search"],
            "page": str(params["page"]),
            "per_page": str(params["per_page"]),
            "Accept": "application/json"
        }
    if request_string == "/organizations":
        return {
            "Authorization": AUTH_COOKIE["Authorization"].value, 
            "name": params["name"],
            "page": str(params["page"]),
            "per_page": str(params["per_page"]),
            "Accept": "application/json"
        }
    return {
        "Authorization": AUTH_COOKIE["Authorization"].value,
        "Accept": "application/json"
    }


def get_request(request_string, token, params):
    request_url = f"{BASE_MS_API_URL}{request_string}" 
    is_wrong_token = validate_token(token)

    if not is_wrong_token:
        try: 
            response = requests.get(
                request_url,
                headers=get_headers(request_string, params)
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
            if request_string == "/user" and response_code == HTTPStatus.OK:
                AUTH_COOKIE["user"] = response_message
            logging.fatal(f"{response_message}")
            return response_message, response_code
    return is_wrong_token


def put_request(request_string, token, data):
    request_url = f"{BASE_MS_API_URL}{request_string}" 
    is_wrong_token = validate_token(token)

    if not is_wrong_token:
        try: 
            response = requests.put(
                request_url, 
                json=data, 
                headers={"Authorization": AUTH_COOKIE["Authorization"].value, "Accept": "application/json"}, 
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
    return is_wrong_token


def validate_token(token):
    if not token:
        return messages.AUTHORISATION_TOKEN_IS_MISSING, HTTPStatus.UNAUTHORIZED
    if AUTH_COOKIE:
        if token != AUTH_COOKIE["Authorization"].value:
            return messages.TOKEN_IS_INVALID, HTTPStatus.UNAUTHORIZED
      

@http_response_namedtuple_converter
def http_response_checker(result):
    # TO DO: REMOVE ALL IF CONDITIONS ONCE ALL BIT-MS HTTP ERROR ISSUES ON MS ARE FIXED 
    # if result.status_code == HTTPStatus.OK:
    #     result = http_ok_status_checker(result)
    # # if result.status_code == HTTPStatus.BAD_REQUEST:
    #     result = http_bad_request_status_checker(result)
    # if result.status_code == HTTPStatus.NOT_FOUND:
    #     result = http_not_found_status_checker(result)
    # if result.status_code == json.dumps(HTTPStatus.INTERNAL_SERVER_ERROR) and not AUTH_COOKIE: 
    #     # if not AUTH_COOKIE:
    #     return messages.TOKEN_IS_INVALID, HTTPStatus.UNAUTHORIZED
    return result


# @http_response_namedtuple_converter
# def http_ok_status_checker(result):
#     # TO DO: REMOVE WHEN ISSUE#619 ON MS BACKEND IS FIXED
#     if result.message == messages.USER_WAS_CREATED_SUCCESSFULLY:
#         return result._replace(status_code=HTTPStatus.CREATED)


# @http_response_namedtuple_converter
# def http_bad_request_status_checker(result):
#     # TO DO: REMOVE ONCE ISSUE#619 ON MS BACKEND IS FIXED
#     if result.message == messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS or result.message == messages.USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS:
#         return result._replace(status_code = HTTPStatus.CONFLICT)


# @http_response_namedtuple_converter
# def http_not_found_status_checker(result):
#     # TO DO: REMOVE ONCE ISSUE#624 ON MS BACKEND IS FIXED
#     if result.message == messages.WRONG_USERNAME_OR_PASSWORD:
#         return result._replace(status_code = HTTPStatus.UNAUTHORIZED)
    
    
