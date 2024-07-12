from ..config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from typing import Coroutine
import uuid
from ..process_input.get_processed_info import InformationBundle
from .image import ImageResizer
from fastapi import UploadFile
import aiohttp


def getFilePreviewUrl(**kwargs):
    baseUrl = 'https://api.apyhub.com/generate/preview/url'
    if not kwargs: return baseUrl
    return f'{baseUrl}?' + '&'.join([f'{key}={value}' for key, value in kwargs.items()])

def getFileUrl(fileId: int):
    return f'{Config.BASE_URL}binary_files/?id={fileId}'

async def getPreview(fileId: int, apiUrl: str, session: AsyncSession):
    # Get file url
    headers = {
        'Content-Type': 'application/json',
        'apy-token': Config.APYHUBTOKEN,
    }
    
    data = {
        'url': getFileUrl(fileId),
    }
    print(apiUrl, data, headers, 'apiUrl, data, headers')
    async with aiohttp.ClientSession() as session:
        async with session.post(apiUrl, json=data, headers=headers) as response:
            response_data = await response.json()
            # return {'preview': response_data['data'], 'id': fileId} # The preview url
            print(response_data, 'response_data')

async def save_file(file: UploadFile) -> Coroutine[None, None, str]:
    """Saves the file to the server and returns the file path."""
    file_extention = file.filename.split('.')[-1]
    file_path = f"./uploads/{str(uuid.uuid4())}.{file_extention}"
    with open(file_path, "wb+") as file_object:
        content = await file.read()  # async read
        file_object.write(content)
    if file_extention in InformationBundle.image_file_types:
        # Will resize the image to maximum supported size by OpenAI 
        # and change its extention if extention is not supported by OpenAI
        file_path = ImageResizer.resize_image(file_path)
        print(file_path, 'file path2')
    return file_path
