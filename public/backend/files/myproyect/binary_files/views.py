import os
from typing import Annotated
from fastapi import APIRouter, Form, UploadFile, HTTPException
from .utils import save_file
from ..aws import s3, dynamodb


binary_files_route = APIRouter(prefix='/api/binary_files', tags=['binary files'])

    
@binary_files_route.post('/')
async def index_post(og_file: Annotated[UploadFile, Form()]):
    file = await save_file(og_file)
    file_name = file['filename']
    file_path = file['filepath']
    s3.upload_file('factic-user-files', file_name, file_path)
    os.remove(file_path)
    save_data = {
        'file_id': file_name,
        'original_file_name': og_file.filename,
    }
    dynamodb.put_item(save_data, 'files')
    return save_data


@binary_files_route.get('/')
def index_get(file_id: str):
    #  check if file_id exists in dynamodb
    existing_item = dynamodb.get_item(key={'file_id': file_id}, table_name='files')
    if not existing_item: raise HTTPException(status_code=404, detail='File not found.')
    return existing_item
