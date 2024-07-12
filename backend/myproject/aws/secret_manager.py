import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os


SECRET_NAMES = {'factic_rds_db_credentials': "rds!cluster-6df27a3a-a7dd-4e0a-88d4-e9ed9cdd9384"}

class SecretManager:
    AWS_REGION = 'us-west-1'
    AWS_SECRETS_ACCESS_KEY_ID = os.getenv('aws_secrets_access_key_id')
    AWS_SECRETS_SECRET_ACCESS_KEY = os.getenv('aws_secrets_secret_access_key')
    def __init__(self) -> None:
        self.session = boto3.Session(
            aws_access_key_id=self.AWS_SECRETS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRETS_SECRET_ACCESS_KEY,
            region_name=self.AWS_REGION,
        )
        # Assume the role
        self.client = self.session.client(service_name='secretsmanager')

    def get_secret(self, secret_name: str) -> str:
        try:
            # Retrieve the secret value
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )

            # Extract the secret value
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = get_secret_value_response['SecretBinary']

            return secret

        except NoCredentialsError:
            print("Credentials not available.")
            return None
        except PartialCredentialsError:
            print("Incomplete credentials provided.")
            return None


secret_manager = SecretManager()
