import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_secret(secret_name: str) -> str:
        session = boto3.Session()
        # Assume the role
        client = session.client(service_name='secretsmanager')
        try:
            # Retrieve the secret value
            get_secret_value_response = client.get_secret_value(
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

db_credentials = json.loads(get_secret('admin-db-credentials'))

class Config:
    document_db_cluster_endpoint = db_credentials['host']
    document_db_username = db_credentials['username']
    document_db_password = db_credentials['password']
    document_db_database = "myAdminData"
    SECRET_KEY = json.loads(get_secret('SECRET_KEY'))['key']
