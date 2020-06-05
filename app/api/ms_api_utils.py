import requests

# from requests.exceptions import HTTPError
from flask import json

from werkzeug.exceptions import HTTPException

# set base url

# for ms-api local server
BASE_MS_API_URL = "http://127.0.0.1:4000"

# create instance
def post_request(request_url, data):
    response = (None,)
    try:

        response_raw = requests.post(
            request_url, json=data, headers={"Accept": "application/json"}
        )
        response_raw.status_code = 201
        response_raw.encoding = "utf-8"
        response = response_raw.json()

    except HTTPException as e:
        response = e.get_response()
        response.data = json.dumps(
            {"code": e.code, "name": e.name, "description": e.description,}
        )
        response.content_type = "application/json"

    print(f"{response}")
    return response