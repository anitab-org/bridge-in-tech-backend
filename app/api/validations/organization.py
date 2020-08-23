from app import messages
from app.utils.bitschema_utils import OrganizationStatus, Timezone, Zone, ProgramStatus
from app.utils.validation_utils import is_email_valid, is_phone_valid
    

def validate_update_organization(data):
    try:
        email = data["email"]
        phone = data["phone"]
        if not is_email_valid(email):
            return messages.EMAIL_INPUT_BY_USER_IS_INVALID
        if not is_phone_valid(phone):
            return messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT
    except ValueError as e:
        return e
    try:
        timezone_value = data["timezone"]
        timezone = Timezone(timezone_value).name
    except ValueError:
        return messages.TIMEZONE_INPUT_IS_INVALID
    except KeyError:
        return messages.TIMEZONE_FIELD_IS_MISSING
    try:
        status_value = data["status"]
        status = OrganizationStatus(status_value).name
    except ValueError:
        return messages.ORGANIZATION_STATUS_INPUT_IS_INVALID
    except KeyError:
        return messages.ORGANIZATION_OR_PROGRAM_STATUS_FIELD_IS_MISSING
    
    
def validate_update_program(data):
    email = data["contact_email"]
    if not email:
        return messages.EMAIL_FIELD_IS_MISSING
    if not is_email_valid(email):
        return messages.EMAIL_INPUT_BY_USER_IS_INVALID
   
    phone = data["contact_phone"]
    if not phone:
        return messages.PHONE_FIELD_IS_MISSING
    if not is_phone_valid(phone):
        return messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT

    mobile = data["contact_mobile"]
    if mobile:
        if not is_phone_valid(mobile):
            return messages.PHONE_OR_MOBILE_IS_NOT_IN_NUMBER_FORMAT
    
    try:
        status_value = data["status"]
        status = ProgramStatus(status_value).name
    except ValueError:
        return messages.PROGRAM_STATUS_INPUT_IS_INVALID
    except KeyError:
        return messages.ORGANIZATION_OR_PROGRAM_STATUS_FIELD_IS_MISSING

   