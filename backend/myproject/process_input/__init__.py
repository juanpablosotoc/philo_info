import json
import uuid
import asyncio
from fastapi import UploadFile
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from myproject.ai import chat
from .get_processed_info import InformationBundle
from ..models import Messages, Texts, Links, Files, LocalOpenaiThreads, LocalOpenaiDb, ProcessedMessageInfo
from ..binary_files import ImageResizer

# Wrapping the UserInput class for encapsulation (it should not be accessed outside of this module)
def wrapper():
    class UserInput:
        def __init__(self, message: Messages, links: list[Links], texts: list[Texts], 
        files: list[Files], 
        openai_db: LocalOpenaiDb, openai_thread: LocalOpenaiThreads) -> None:
            self.message = message
            self.openai_db = openai_db
            self.openai_thread = openai_thread
            self.information_bundle = InformationBundle(texts=texts, links=links, files=files, 
                                                        openai_db=openai_db, openai_thread=openai_thread)
        
        async def get_output_combinations(self, processed_info: str) -> str:
            """Returns the output combinations as a dictionary for a given processed info."""
            # Get the prompt messages
            messages = chat.get_possible_output_choices(processed_message_info=processed_info)
            # Get the output combinations from openai
            response = await chat.ask.no_stream(messages=messages)
            # Return the output combinations as a dictionary
            return response

        async def store_processed_info(self, session: AsyncSession, processed_info: str) -> None:
            """Stores the processed info in the database."""
            processed_message_info = ProcessedMessageInfo(message_id=self.message.id, text=processed_info)
            session.add(processed_message_info)
            await session.commit()

        async def processed_info_output_combos(self, session: AsyncSession):
            """Streams the processed information."""
            # Yield the processed info
            processed_info_dict: dict = {item.id: '' for item in self.information_bundle.items}
            done = {item.id: False for item in self.information_bundle.items}
            processed_infos: dict[str, AsyncGenerator ] = {item.id: item.processed_info() for item in self.information_bundle.items}
            items_iterator = self.information_bundle.items.__iter__()
            while True:
                try:
                    item = items_iterator.__next__()
                except StopIteration:
                    items_iterator = self.information_bundle.items.__iter__()
                if all(done.values()): break
                if done[item.id or not item.ready]: continue
                # We know that item is ready and hasnt been fully processed
                try:
                    item_value = await anext(processed_infos[item.id])
                    processed_info_dict[item.id] += item_value
                    yield json.dumps(({'type': 'processed_info', 'id': item.id, 'info': item_value}))
                except StopAsyncIteration:
                    done[item.id] = True
            processed_info = '\n'.join([processed_info_dict[item.id] for item in self.information_bundle.items])
            await self.store_processed_info(session=session, processed_info=processed_info)   
            # Yiel the output combinations (should not be streamed)
            output_combinations = await self.get_output_combinations(processed_info=processed_info)
            output_combinations = json.loads(output_combinations)
            yield json.dumps({'type': 'choices', **output_combinations})
    
    async def user_input_factory(links_strs: list[str], texts_strs: list[str], files: list[Files], 
        session: AsyncSession, openai_thread: LocalOpenaiThreads, openai_db: LocalOpenaiDb):
        """This function is a factory function that creates a UserInput object from the
        user input. The user input can be in the form of 'links', 'texts', and files.
        The links and texts should be in the form of a list of strings.
        The file_storage_objs should be in the form of a list of UploadFile objects.
        The function will return a UserInput object."""
        # Get the questions and texts from the user input. 
        # A question is a string that starts with "/explain "
        # Create the message and add it to the database
        message = Messages(thread_id=openai_thread.thread_id)
        session.add(message)
        await session.commit()
        # Create the texts, links, questions, and files and add them to the database
        texts = [Texts(text=text, message_id=message.id) for text in texts_strs]
        links = [Links(link=link, message_id=message.id) for link in links_strs]
        session.add_all(texts)
        session.add_all(links)
        # Create the user input object
        user_input = UserInput(links=links, message=message, texts=texts, files=files, openai_thread=openai_thread, openai_db=openai_db)
        # Commit the changes to the database
        await session.commit()
        return user_input
    
    return user_input_factory

# UserInputFactory is an async factory function that creates a UserInput object
UserInputFactory = wrapper()
