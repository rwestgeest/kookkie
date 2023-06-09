import os

import boto3 # type: ignore
from botocore.exceptions import ClientError # type: ignore


class AWSBasedSecrets:
    @property
    def jitsi_private_key(self):
        secret_name = "prod/kookkie/jitsipk"
        region_name = "eu-central-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        return get_secret_value_response['SecretString']


class LocalSecrets:
    def __init__(self, location):
        self._location = location

    @property
    def jitsi_private_key(self):
        with open(self._location) as f:
            return f.read()
