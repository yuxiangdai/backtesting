import holidays
import datetime

holidays = holidays.UnitedStates() +  holidays.Canada()

def sanitize_dates(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    if not date.weekday() < 5:
        date = date + datetime.timedelta(days=2)
    if date in holidays:
        date = date + datetime.timedelta(days=1)

    return date.strftime("%Y-%m-%d")
    # return datetime.datetime.timestamp(date) 

def shift_date_string(date_string, num):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    date = date + datetime.timedelta(days=num)
    return date.strftime("%Y-%m-%d")

def date_to_timestamp(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return datetime.datetime.timestamp(date) 