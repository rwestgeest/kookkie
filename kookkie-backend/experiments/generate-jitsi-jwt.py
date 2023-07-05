#!/bin/env python
import os

from app.utils.jaas_jwt_builder import JaaSJwtBuilder
from tests.domain.builders import aValidKook

print(JaaSJwtBuilder(
    app_id=os.getenv('JITSI_APP_ID'),
    api_key=os.getenv('JITSI_API_KEY'),
    private_key=os.getenv('JITSI_PRIVATE_KEY')
).for_guest("Harry", "LekkerEtenMetRob"))