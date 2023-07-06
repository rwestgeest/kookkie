#!/bin/env python
import os

from app.utils.jaas_jwt_builder import JaaSJwtBuilder
from tests.domain.builders import aValidKook

def read_pk():
    with open("/home/rob/.ssh/jitsi.pk") as f:
        return f.read()
    
result = JaaSJwtBuilder(
    app_id=os.getenv('JITSI_APP_ID'),
    api_key=os.getenv('JITSI_API_KEY'),
    private_key=read_pk()
).for_kook(aValidKook(name="Rob Westgeest", email="rob@qwan.eu"), "KikkererwtenMetKoesKoes")
print(result)
