import asyncio
from asyncio import Task
from typing import Annotated
from sqlalchemy.future import select
import uuid
from myproject import user_db_dependancy, db_dependancy
from ..models import Files
from ..config import Config
from .utils import getFilePreviewUrl, getPreview, save_file
from fastapi import APIRouter, Form, HTTPException, UploadFile
import aiohttp
import asyncio

binary_files_route = APIRouter(prefix='/binary_files', tags=['binary files'])

    
@binary_files_route.post('/')
async def index_post(file: Annotated[UploadFile, Form()], user_db: user_db_dependancy):
    async with asyncio.TaskGroup() as tg:
        file_task = tg.create_task(save_file(file))
    fileDbObject = Files(path=file_task.result())
    user_db.session.add(fileDbObject)
    await user_db.session.commit()
    async with asyncio.TaskGroup() as tg:
        getPreviewTask = tg.create_task(getPreview(fileDbObject.id, apiUrl=getFilePreviewUrl(**Config.FILEPREVIEWDEFAULTOPTIONS), session=user_db.session))
    preview = getPreviewTask.result()
    url = preview['preview']
    # Save the image from that url
    file_path = f"./uploads/{str(uuid.uuid4())}.png"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(file_path, "wb") as file:
                file.write(await response.content.read())
    fileDbObject.preview_path = file_path
    
    await user_db.session.commit()
    user_db.close_session() # Close the session
    return {'id': fileDbObject.id}
