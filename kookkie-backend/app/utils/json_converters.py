from datetime import date
import re
import json


def default_dumper(obj):
    if type(obj) is date:
        return obj.isoformat()


def date_parser(json_dict):
    for (key, value) in json_dict.items():
        if type(value) is str and re.match('^\d{4}-\d{2}-\d{2}', value):
            json_dict[key] = date.fromisoformat(value)
        else:
            pass
    return json_dict


def json_dumps(obj):
    return  json.dumps(obj, default=default_dumper)


def json_loads(obj):
    return json.loads(obj)
