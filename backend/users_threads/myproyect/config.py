import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


FACTIC_DB_CREDENTIALS = 'rds!cluster-f1c68034-26d2-43e3-82af-15ebec700a28'
DB_NAME = 'users_threads'
AWS_REGION = os.getenv('AWS_DEFAULT_REGION')
USER_ID = os.getenv('aws_account_id')
DEL_USER_QUEUE_NAME = 'DelUserMessagesQueue'

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


db_secret = json.loads(get_secret(FACTIC_DB_CREDENTIALS))
db_username = db_secret['username']
db_password = db_secret['password']


class Config:
    SECRET_KEY = json.loads(get_secret('SECRET_KEY'))['key']
    DB_URI = os.getenv('db_uri')
    SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://{db_username}:{db_password}@{DB_URI}:3306/{DB_NAME}"
    DEL_SQS_QUEUE = f'https://sqs.{AWS_REGION}.amazonaws.com/{USER_ID}/{DEL_USER_QUEUE_NAME}'
