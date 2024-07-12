import boto3
import os
from enum import Enum


class S3Bucket(Enum):
    factic_file_previews = 'factic-file-previews'
    

class S3:
    AWS_REGION = 'us-west-1' # Northern California
    AWS_S3_ACCESS_KEY_ID = os.getenv('aws_s3_access_key_id')
    AWS_S3_SECRET_ACCESS_KEY = os.getenv('aws_s3_secret_access_key')
    def __init__(self) -> None:
        # Initialize a session using the credentials of the IAM user
        self.session = boto3.Session(
            aws_access_key_id=self.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_S3_SECRET_ACCESS_KEY,
            region_name=self.AWS_REGION
        )
        # Assume the role
        client = self.session.client('sts')
        self.role = client.assume_role(
            RoleArn='arn:aws:iam::471112820692:role/s3_full_access',
            RoleSessionName='LocalS3AccessSession'
        )
        # Use the temporary credentials to create an S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.role['Credentials']['AccessKeyId'],
            aws_secret_access_key=self.role['Credentials']['SecretAccessKey'],
            aws_session_token=self.role['Credentials']['SessionToken']
        )

    def get_buckets(self) -> str:
        # Now you can perform S3 operations
        response = self.s3_client.list_buckets() 
        return response['Buckets']
    
    def create_bucket(self, bucket_name: str) -> None:
        # Create a bucket
        self.s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': self.AWS_REGION
            }
        )
        print(f'Bucket {bucket_name} created successfully.')

    def upload_file(self, bucket_name: S3Bucket, object_name: str, file_path: str) -> None:
        self.s3_client.upload_file(file_path, bucket_name.value, object_name)

        print(f'File {file_path} uploaded to bucket {bucket_name} as {object_name}.')

    def download_file(self, bucket_name: str, object_name: str, download_path: str) -> None:
        self.s3_client.download_file(bucket_name, object_name, download_path)

        print(f'File {object_name} downloaded from bucket {bucket_name} to {download_path}.')

    @classmethod
    def generate_public_url(cls, bucket_name: str, object_name: str) -> None:
        return f"https://{bucket_name}.s3.{cls.AWS_REGION}.amazonaws.com/{object_name}"


s3 = S3()
