import datetime
import pytz
import dateutil.parser


def convert_timestamp_to_human_date(unix_time, timezone):
    date = datetime.datetime.utcfromtimestamp(unix_time)
    date_with_utc_timezone = pytz.UTC.localize(date)
    user_timezone = pytz.timezone(timezone)
    date_in_user_timezone = date_with_utc_timezone.astimezone(user_timezone)
    date_format = "%Y-%m-%d %H:%M %Z%z"
    return date_in_user_timezone.strftime(date_format)


def convert_human_date_to_timestamp(input_date, timezone):
    try:
        user_input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M")
        user_timezone = pytz.timezone(timezone)
        date_in_user_timezone = user_timezone.localize(user_input_date)
        utc_timezone = pytz.UTC
        date_in_utc_timezone = date_in_user_timezone.astimezone(utc_timezone)
        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD HH:MM")
    
    return (date_in_utc_timezone - epoch).total_seconds()




    
