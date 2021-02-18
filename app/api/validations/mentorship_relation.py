from app import messages

def org_mentee_req_body_is_valid_data(data):

    # Verify if request body has required fields
    if "mentee_id" not in data:
        return messages.MENTEE_ID_FIELD_IS_MISSING
    if "end_date" not in data:
        return messages.END_DATE_FIELD_IS_MISSING
    if "notes" not in data:
        return messages.NOTES_FIELD_IS_MISSING
    if "mentee_request_date" not in data:
        return messages.MENTEE_REQUEST_DATE_FIELD_IS_MISSING
    return {}