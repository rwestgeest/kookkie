from quiltz.domain.results import Success, Failure
from datetime import date


def create_date_from_string(string_value, name='date'):
    if string_value is None: return Failure(message="{} is missing".format(name))
    try: 
        return Success(date=date.fromisoformat(string_value))
    except ValueError as e:
        return Failure(message='{} is not a valid date'.format(name))
