
class Prompts:
    create_file_search_assistant_instr = "You are a very helpful assistant who will give me a detailed summary of the information in the documents that I have uploaded."
    output_guide = """
    1. text: Is a very versatile way to represent information.
    2. timeline: Works best when representing a sequence of events.
    3. table: Works best when comparing different items.
    4. speech: Is a very versatile way to represent information.
    5. list: Works best when listing items.
    """
    @staticmethod
    def get_user_message(content: str) -> dict:
        return {'role': 'user', 'content': content}
    
    @staticmethod
    def process_link_messages(link: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of what the following website is about:
        {link}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_text_messages(text: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of the text denoted by [[[ ]]]. 
        [[[ 
            {text} 
        ]]]
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_transcript_messages(transcript: str) -> list:
        human_message_str = f"""
        Give me a very detailed summary of the following transcript:
        {transcript}
        """
        return [{"role": "user", "content": human_message_str}]
        
    @staticmethod
    def process_document_messages(message_file) -> list:
        mes = [{
        "role": "user",
        "content": "Give me a detailed summary of the information in the following document.",
        # Attach the new file to the message.
        "attachments": [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
        }]
        return mes
    
    @staticmethod
    def process_image_messages(base64_image: str, detail='auto') -> list:
        return [
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "Give me a detailsed summary of the information portrayed in the following image:"},
                {
                "type": "image_url",
                "image_url": {
                    'url': f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail
                },
                },
            ],
            }
        ]
    
    @staticmethod
    def ask_assistant_file_search_messages(file_ids: list = []) -> list:
        messages = [{
            "role": "user",
            "content": "Give me a very detailed description of the information in the documents that I have uploaded.",
        }]
        # Attach a new file to the message.
        if len(file_ids) > 0: messages[0]['attachments'] = []
        for file_id in file_ids:
            messages[0]['attachments'].append({ "file_id": file_id, "tools": [{"type": "file_search"}] })
        return messages
    
    @staticmethod
    def get_questions_topics(n_topics: int, n_questions: int, dont_include_topics: list[str]) -> list:
        messages = [
            {
                'role': 'system',
                'content': 'You are a very useful assistant who will respond only using json.'
            },
            {
                'role': 'user',
                'content': f'Give me a list of 2 topics along with 3 short and interesting questions related to each topic.'
            },
            {
                'role': 'assistant',
                'content': """{
                    "topics": [
                        {
                            "topic": "Topic 1",
                            "questions": [
                                "Question 1",
                                "Question 2",
                                "Question 3"
                            ]
                        },
                        {
                            "topic": "Topic 2",
                            "questions": [
                                "Question 1",
                                "Question 2",
                                "Question 3"
                            ]
                        }
                    ]
                }"""
            },
            {
                'role': 'user',
                'content': f'Give me a list of {n_topics} topics along with {n_questions} short and interesting questions related to each topic.  Do not include the following topics: {dont_include_topics}'
            },
        ]
        return messages
    
    @staticmethod
    def get_questions_for_topic(topic: str, n_questions: int) -> list:
        messages = [
            {
                'role': 'system',
                'content': 'You are a very useful assistant who will respond only using json. Do not prefix your responses with ```json'
            },
            {
                'role': 'user',
                'content': f'Give me a list of 3 short and interesting questions related to the topic "topic".'
            },
            {
                'role': 'assistant',
                'content': """
                    {
                        "questions": [
                        "Question 1",
                        "Question 2",
                        "Question 3"
                    ]
                    }
                """
            },
            {
                'role': 'user',
                'content': f'Give me a list of {n_questions} short and interesting questions related to the topic "{topic}".'
            },
        ]
        return messages
    
    def get_output_combinations(cls, processed_message_info: str) -> list:
        messages = [
            {
                'role': 'system',
                'content': f"""You are a very useful teacher who will respond only using json. 
                Do not prefix your responses with ```json. 
                You will help me choose the best way to represent information given the information type. 
                Use the following guide to help you choose in which way the information can be best represented:
                {cls.output_guide}"""
            },
            {
                'role': 'user',
                'content': f"""The text between [[[ ]]] is a summary of a document. 
                Please tell me in wich way I could best represent the information in the document to make it interesting. 
                Use the following guide to help you choose in which way the information can be best represented:
                {cls.output_guide}
                

                [[[ {processed_message_info} ]]]"""
            },
        ]
        return messages
    