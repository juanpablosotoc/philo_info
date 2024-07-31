import uuid
from fastapi import UploadFile
from .image import ImageResizer
from ..config import Config


async def save_file(file: UploadFile) -> str:
    """Saves the file to the server and returns the file path."""
    file_extention = file.filename.split('.')[-1]
    new_file_name = f'{str(uuid.uuid4())}.{file_extention}'
    file_path = f"./uploads/{new_file_name}"
    with open(file_path, "wb+") as file_object:
        content = await file.read()  # async read
        file_object.write(content)
    if file_extention in Config.image_file_types:
        # Will resize the image to maximum supported size by OpenAI 
        # and change its extention if extention is not supported by OpenAI
        file_path = ImageResizer.resize_image(file_path)
    return {'filename': new_file_name, 'filepath': file_path}
