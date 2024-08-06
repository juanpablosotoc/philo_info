import boto3
from typing import Literal
from .config import Config


class S3:
    def get_s3_client(self):
        return boto3.client('s3')

    def upload_file(self, bucket_name: Literal['factic-user-files', 'factic-user-previews'], object_name: str, file_path: str) -> None:
        client = self.get_s3_client()
        client.upload_file(file_path, bucket_name, object_name)

        print(f'File {file_path} uploaded to bucket {bucket_name} as {object_name}.')

    def download_file(self, bucket_name: Literal['factic-user-files', 'factic-user-previews'], object_name: str, file_path: str) -> None:
        client = self.get_s3_client()
        client.download_file(bucket_name, object_name, file_path)

        print(f'File {object_name} downloaded from bucket {bucket_name} to {file_path}.')

    @staticmethod
    def generate_public_url(bucket_name: Literal['factic-user-files', 'factic-user-previews'], object_name: str) -> None:
        return f"https://{bucket_name}.s3.{Config.AWS_REGION}.amazonaws.com/{object_name}"


class DynamoDB:
    def get_table(self, table_name: str):
        # Create a DynamoDB resource
        dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)    
        # Specify the table you want to interact with
        return dynamodb.Table(table_name)
    
    def put_item(self, item: dict, table_name: str) -> None:
        table = self.get_table(table_name)
        table.put_item(Item=item)
    
    def get_item(self, key: dict, table_name: str) -> dict:
        table = self.get_table(table_name)
        response = table.get_item(Key=key)
        return response.get('Item', None)
    

s3 = S3()
dynamodb = DynamoDB()
