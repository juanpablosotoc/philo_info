import json
import uuid
import asyncio
from asyncio import Task
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from myproject.ai import chat
from .get_processed_info import InformationBundle, Question
from ..models import Messages, Texts, Links, Files, MessageQuestions, LocalOpenaiThreads, LocalOpenaiDb, ProcessedMessageInfo
from ..binary_files import ImageResizer

# Wrapping the UserInput class for encapsulation (it should not be accessed outside of this module)
def wrapper():
    class UserInput:
        def __init__(self, message: Messages, links: list[Links], texts: list[Texts], 
        files: list[Files], message_questions: list[MessageQuestions], type_id: int, 
        openai_db: LocalOpenaiDb, openai_thread: LocalOpenaiThreads) -> None:
            self.type_id = type_id
            self.message = message
            self.openai_db = openai_db
            self.openai_thread = openai_thread
            if type_id == 2: # is information bundle
                self.information_bundle = InformationBundle(texts=texts, links=links, files=files, openai_db=openai_db, openai_thread=openai_thread)
            else: # is question
                self.message_questions = message_questions
                self.questions = [Question(question) for question in self.message_questions]
        
        async def processed_info(self, session: AsyncSession):
            """Returns the processed information as a string."""
            if self.type_id == 1: # is question
                tasks: list[Task] = []
                # Get all the question information asynchronously
                async with asyncio.TaskGroup() as tg:
                    for question in self.questions:
                        tasks.append(tg.create_task(question.process_info()))
                # Return the information as a string
                return ''.join([task.result() for task in tasks])
            # is information bundle
            information_bundle_processed_info: str = await self.information_bundle.process_info(session=session)
            return information_bundle_processed_info
        
        async def get_output_combinations(self, processed_info: str) -> dict:
            """Returns the output combinations as a dictionary for a given processed info."""
            # Get the prompt messages
            messages = chat.get_output_combinations_messages(processed_message_info=processed_info)
            # Get the output combinations from openai
            response = await chat.ask.no_stream(messages=messages)
            # Return the output combinations as a dictionary
            return json.loads(response)

        async def store_processed_info(self, session: AsyncSession, processed_info: str) -> None:
            """Stores the processed info in the database."""
            processed_message_info = ProcessedMessageInfo(message_id=self.message.id, text=processed_info)
            session.add(processed_message_info)
            await session.commit()

        async def process_get_output_combinations(self, session: AsyncSession) -> dict:
            """Returns the output combinations for the user input."""
            # Get the processed information
            processed_info: str = await self.processed_info(session=session)
            # Store the processed information in the database and
            # get the output combinations
            async with asyncio.TaskGroup() as tg:
                output_combinations_task = tg.create_task(self.get_output_combinations(processed_info=processed_info))
                tg.create_task(self.store_processed_info(session=session, processed_info=processed_info))
            return output_combinations_task.result()
              
    async def save_file(file: UploadFile) -> str:
        """Saves the file to the server and returns the file path.
        file_path: The path to save the file to."""
        file_extention = file.filename.split('.')[-1]
        file_path = f"./uploads/{str(uuid.uuid4())}.{file_extention}"
        with open(file_path, "wb+") as file_object:
            content = await file.read()  # async read
            await file_object.write(content)
        if file_extention in InformationBundle.image_file_types:
            # Will resize the image to maximum supported size by OpenAI 
            # and change its extention if extention is not supported by OpenAI
            file_path = ImageResizer.resize_image(file_path)
        return file_path
    
    async def user_input_factory(links_strs: list[str], texts_strs: list[str], file_storage_objs: list[UploadFile], 
        session: AsyncSession, openai_thread: LocalOpenaiThreads, openai_db: LocalOpenaiDb):
        """This function is a factory function that creates a UserInput object from the
        user input. The user input can be in the form of 'links', 'texts', and files.
        The links and texts should be in the form of a list of strings.
        The file_storage_objs should be in the form of a list of UploadFile objects.
        The function will return a UserInput object."""
        # Get the questions and texts from the user input. 
        # A question is a string that starts with "/explain "
        questions_strs = [text for text in texts_strs if text.startswith("/explain ")]
        texts_strs = [text for text in texts_strs if not text.startswith("/explain ")]
        # Check if the user input is a question or information bundle
        type_id = 2 # Sets message type to information bundle
        if len(questions_strs) > 0: type_id = 1 # Sets message type to question
        # Create the message and add it to the database
        message = Messages(thread_id=openai_thread.thread_id, type_id=type_id)
        session.add(message)
        await session.commit()
        if type_id == 1:
            # Message type is question
            # Create the message questions and add them to the database
            message_questions = [MessageQuestions(question=question, message_id=message.id) for question in questions_strs]
            session.add_all(message_questions)
            # Create the user input object
            user_input = UserInput(message_questions=message_questions, message=message, links=[], texts=[], 
                        files=[], type_id=type_id, openai_db=openai_db, openai_thread=openai_thread)
        else:
            # Message type is information bundle
            # Create the texts, links, and files and add them to the database
            texts = [Texts(text=text, message_id=message.id) for text in texts_strs]
            links = [Links(link=link, message_id=message.id) for link in links_strs]
            files = []
            file_tasks = []
            async with asyncio.TaskGroup() as tg:
                for file_store_obj in file_storage_objs:
                    file_tasks.append(tg.create_task(save_file(file_store_obj)))
            for new_file_path in [task.result() for task in file_tasks]:
                files.append(Files(path=new_file_path, message_id=message.id))
            session.add_all(texts)
            session.add_all(links)
            session.add_all(files)
            # Create the user input object
            user_input = UserInput(links=links, message=message, texts=texts, files=files, message_questions=[], type_id=type_id, openai_thread=openai_thread, openai_db=openai_db)
        # Commit the changes to the database
        await session.commit()
        return user_input
    
    return user_input_factory

# UserInputFactory is an async factory function that creates a UserInput object
UserInputFactory = wrapper()
