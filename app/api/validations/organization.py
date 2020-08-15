from app import messages
from app.utils.bitschema_utils import *
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
        return messages.STATUS_INPUT_IS_INVALID
    except KeyError:
        return messages.ORGANIZATION_STATUS_FIELD_IS_MISSING
    
    
     