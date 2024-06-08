from .get_processed_info import InformationBundle, Question
from ..models import Messages, Texts, Links, Files, MessageQuestions
from werkzeug.datastructures import FileStorage
import uuid
from myproject.ai import chat
import json
from ..binary_files import ImageResizer
from sqlalchemy.ext.asyncio import AsyncSession


class UserInput:
    def __init__(self, links: list[Links], texts: list[Texts], files: list[Files], message_questions: list[MessageQuestions], type_id: int) -> None:
        self.type_id = type_id
        if type_id == 2: # is information bundle
            self.texts = texts
            self.links = links
            self.files = files
            self.information_bundle = InformationBundle(texts=self.texts, links=self.links, files=self.files)
        else:
            self.message_questions = message_questions
            self.questions = [Question(question) for question in self.message_questions]
    
    async def info(self, session: AsyncSession):
        if self.type_id == 1: 
            question_infos = ''
            for question in self.questions:
                question_infos += await question.info() + '\n'
            return question_infos
        return await self.information_bundle.info(session=session)
    
    async def get_output_combinations(self, session: AsyncSession):
        return json.loads(await chat.ask.no_stream(chat.get_output_combinations(await self.info(session=session))))
    

async def user_input_factory(links_strs: list[str], texts_strs: list[str], file_storage_objs: list[FileStorage], thread_id: int, session: AsyncSession):
    questions_strs = [text for text in texts_strs if text.startswith("/explain ")]
    texts_strs = [text for text in texts_strs if not text.startswith("/explain ")]
    type_id = 2 # Sets message type to information bundle
    if len(questions_strs) > 0: type_id = 1 # Sets message type to question
    message = Messages(thread_id=thread_id, type_id=type_id)
    session.add(message)
    await session.commit()
    if type_id == 1:
        message_questions = [MessageQuestions(question=question, message_id=message.id) for question in questions_strs]
        session.add_all(message_questions)
        await session.commit()
        user_input = UserInput(message_questions=message_questions, links=[], texts=[], files=[], type_id=type_id )
    else:
        texts = [Texts(text=text, message_id=message.id) for text in texts_strs]
        links = [Links(link=link, message_id=message.id) for link in links_strs]
        files = []
        for file_store_obj in file_storage_objs:
            file_extention = file_store_obj.filename.split('.')[-1]
            file_path = f"./uploads/{str(uuid.uuid4())}.{file_extention}"
            file_store_obj.save(file_path)
            if file_extention in InformationBundle.vision_file_types:
                ImageResizer.resize_image(file_path)
            files.append(Files(path=file_path, message_id=message.id))
        session.add_all(texts)
        session.add_all(links)
        session.add_all(files)
        await session.commit()
        user_input = UserInput(links=links, texts=texts, files=files, message_questions=[], type_id=type_id)
    return user_input