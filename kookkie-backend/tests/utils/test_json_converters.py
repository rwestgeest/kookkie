from datetime import date
from app.utils.json_converters import json_dumps, json_loads

def test_json_dumps_converts_dates_to_iso_dates():
    assert json_dumps(dict(the_date = date(year=2018, month=12,day=23))) == '{"the_date": "2018-12-23"}'

def xtest_json_loads_converts_from_iso_dates():
    assert json_loads('{"the_date": "2018-12-23"}') == dict(the_date = date(year=2018, month=12,day=23))