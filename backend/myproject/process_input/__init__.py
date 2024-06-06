from .get_processed_info import InformationBundle, Question
from ..models import Messages, Texts, Links, Files, MessageQuestions
from werkzeug.datastructures import FileStorage
import uuid
from myproject.ai import chat, db
import json
from ..binary_files import ImageResizer

class UserInput:
    def __init__(self, links_strs: list[str], texts_strs: list[str], files_filestorages: list[FileStorage], thread_id: int) -> None:
        texts = [text for text in texts_strs if not text.startswith("/explain ")]
        questions = [text for text in texts_strs if text.startswith("/explain ")]
        type_id = 2 # Sets message type to information bundle
        if len(questions) > 0: type_id = 1 # Sets message type to question
        self.message = Messages(thread_id=thread_id, type_id=type_id)
        db.session.add(self.message)
        db.session.commit()
        if type_id == 2: # is information bundle
            self.links = [Links(link=link,  message_id=self.message.id) for link in links_strs]
            self.texts = [Texts(text=text, message_id=self.message.id) for text in texts]
            self.files = []
            for file_store_obj in files_filestorages:
                file_extention = file_store_obj.filename.split('.')[-1]
                file_path = f"./backend/uploads/{str(uuid.uuid4())}.{file_extention}"
                file_store_obj.save(file_path)
                if file_extention in InformationBundle.vision_file_types:
                    ImageResizer.resize_image(file_path)
                self.files.append(Files(path=file_path, message_id=self.message.id))
            db.session.add_all(self.links)
            db.session.add_all(self.texts)
            db.session.add_all(self.files)
            db.session.commit()
            self.information_bundle = InformationBundle(texts=self.texts, links=self.links, files=self.files)
        else:
            self.message_questions = [MessageQuestions(question=question, message_id=self.message.id) for question in questions]
            db.session.add_all(self.message_questions)
            db.session.commit()
            self.questions = [Question(question) for question in self.message_questions]
    
    @property
    def info(self):
        if self.message.type_id == 1: 
            question_infos = ''
            for question in self.questions:
                question_infos += question.info + '\n'
            return question_infos
        return self.information_bundle.info 
    
    def get_output_combinations(self):
        return json.loads(chat.ask.no_stream(chat.get_output_combinations(self.info)))
    