"""This module is to check the validity of input for the "name", "email", "username" fields
against predetermined patterns as well as to ensure the string input is within the accepted length.

For the "name" field to be valid, it may contain one or more character from:
- letter "a" to "z" and/or "A" to "Z", 
- any of the whitespace characters, and/or
- special character "-".

For the "email" field to be valid, it must have the following structure:
> the first section, which may contain one or more character from:
    - letter "a" to "z" and/or "A" to "Z",
    - number "0" to "9",
    - special character "_", ".", "+", and/or "-".
> followed by the "@" character,
> followed by the second section, which may contain one or more character from:
    - letter "a" to "z" and/or "A" to "Z",
    - number "0" to "9", and/or
    - special character "-".
> followed by the escaped character ".",
> followed by the third section, which may contain one or more character from:
    - letter "a" to "z" and/or "A" to "Z",
    - number "0" to "9",
    - special character "-" and/or ".".

For the "username" field to be valid, it may contain one or more character from:
    - letter "a" to "z" and/or "A" to "Z",
    - number "0" to "9", and/or
    - special character "-".

For the "phone" or "mobile" field to be valid, it must have the following format:
    - must contain numbers from "0" to "9" 
    - may contain one or more character from special character "-"
    - may contain one or more character from whitespace " "
"""
import re
from app import messages


name_regex = r"(^[a-zA-Z\s\-]+$)"
email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_regex = r"(^[a-zA-Z0-9_]+$)"
phone_regex = r"(^[0-9\s\-\+]+$)"

def is_name_valid(name):
    """Checks if name input is within the acceptable pattern defined in name_regex.
    
    Args:
        name: string input for name.
    
    Return:
        True: if string input for name is within the acceptable name_regex pattern.
        False: if string input for name is not according to name_regex pattern.
    """
    return re.match(name_regex, name)


def is_email_valid(email):
    """Checks if email input is within the acceptable pattern defined in email_regex.
    
    Args:
        email: string input for email.
    
    Return:
        True: if string input for email is within the acceptable email_regex pattern.
        False: if string input for email is not according to email_regex pattern.
    """
    return re.match(email_regex, email)


def is_username_valid(username):
    """Checks if username input is within the acceptable pattern defined in username_regex.
    
    Args:
        name: string input for username.
    
    Return:
        True: if string input for username is within the acceptable username_regex pattern.
        False: if string input for username is not according to username_regex pattern.
    """
    return re.match(username_regex, username)

def validate_length(field_length, min_length, max_length, field_name):
    """Validates string input.

    Checks the length of the string which is inserted in a particular field against the given values.

    Args: 
        field_length: length of the string input in a given field.
        min_length: minimum acceptable string length. 
        max_length: maximum acceptable string length.
        field_name: the name of the field where the string is inserted.

    Returns:
        False, error_msg: if string input is either less than the minimum length, or more than the maximum length.
        True, {}: if string input is longer or equals to the minimum length, and less than or equals to the maximum length. 
    """
    if not min_length <= field_length <= max_length:
        if min_length <= 0:
            error_msg = {
                "message": get_length_validation_error_message(
                    field_name, None, max_length
                )
            }
        
        error_msg = {
            "message": get_length_validation_error_message(
                field_name, min_length, max_length
            )
        }
        return {"is_valid": False, "message": error_msg}
    
    return {"is_valid": True, "message": {}}


def get_length_validation_error_message(field_name, min_length, max_length):
    """Returns an error message which content depends on the given keys.

    Args:
        field_name: the name of the field where the string is inserted.
        min_length: minimum acceptable string length. 
        max_length: maximum acceptable string length.
    
    Returns:
        - error message if minimum length is not determined.
        - error message if minimum length is determined.
    """
    if min_length is None:
        return f"The {field_name} field has to be no more than {max_limit} characters."
        
    
    return f"The {field_name} field has to be at least {min_length} characters and no more than {max_length} characters."
    


def get_stripped_string(string_with_whitespaces):
    """Returns a new string from key argument that has been cleaned from whitespaces (split and joined by delimiter "").
    
    Args:
        string_with_whitespaces: string input that has whitespaces.

    Return:
        A new string which is the string_with_whitespaces with whitespaces been removed.
    """
    return "".join(string_with_whitespaces.split())

def expected_fields_validator(user_input, data_model):
    """Validates data fields. Confirms whether or not user input fields contains only the expected fields of the data model.
    
    Args:
        user_input: A list of keys of all fields that are submitted by user to the payload. 
        data_model: A list of keys of all fields that are expected to be on the payload.
        
    Return:
        False, error_message: A dictionary with a boolean value stating input fields are not valid and an error message. 
        True, {}: A dictionary with a boolean value stating input fields are valid and no other message given.
    """
    expected_fields = []
    for field_input in user_input:
        for field_expected in data_model:
            if field_input == field_expected:
                expected_fields.append(field_input)
    if len(expected_fields) != len(data_model):
        return {"is_field_valid": False, "message": messages.UNEXPECTED_INPUT}
    return {"is_field_valid": True, "message": {}}

def is_phone_valid(phone):
    """Checks if phone or mobile input is within the acceptable pattern defined in phone_regex.
    
    Args:
        name: string input for phone or mobile.
    
    Return:
        True: if string input for phone or mobile is within the acceptable phone_regex pattern.
        False: if string input for phone or mobile is not according to phone_regex pattern.
    """
    return re.match(phone_regex, phone)
