# This class is used to store the prompts for the Openai calls.
class Prompts:
    # The output guide is used to determine the best way to represent information
    output_guide = """
    1. text: Is a very versatile way to represent information.
    2. timeline: Works best when representing a sequence of events.
    3. table: Works best when comparing different items.
    4. speech: Is a very versatile way to represent information.
    5. list: Works best when listing items.
    """
    @staticmethod
    def get_user_message(content: str) -> dict:
        """Returns a user message."""
        return {'role': 'user', 'content': content}
    
    @staticmethod
    def process_link_messages(link: str) -> list:
        """Returns a list of messages that ask the assistant to process a link."""
        human_message_str = f"""
        Give me a detailed summary of what the following website is about:
        {link}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_text_messages(text: str) -> list:
        """Returns a list of messages that ask the assistant to process a text."""
        human_message_str = f"""
        Give me a detailed summary of the text denoted by [[[ ]]]. 
        [[[ 
            {text} 
        ]]]
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_transcript_messages(transcript: str) -> list:
        """Returns a list of messages that ask the assistant to process a transcript."""
        human_message_str = f"""
        Give me a very detailed summary of the following transcript:
        {transcript}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_image_messages(base64_image: str, detail='auto') -> list:
        """Returns a list of messages that ask the assistant to process a base64 image."""
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
    def ask_assistant_file_search_messages() -> list:
        """Returns a list of messages that ask the assistant to process the 
        files inside its vector store."""
        messages = [{
            "role": "user",
            "content": "Give me a very detailed description of the information in the documents that I have uploaded.",
        }]
        return messages
    
    @staticmethod
    def get_questions_topics_messages(n_topics: int, n_questions: int, dont_include_topics: list[str]) -> list:
        """Returns a list of messages that ask the assistant to provide a list of questions and topics."""
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
                'content': f'Give me a list of {n_topics} easy and interesting topics along with {n_questions} very short and interesting questions related to each topic.  Do not include the following topics: {dont_include_topics}'
            },
        ]
        return messages
    
    @staticmethod
    def get_questions_for_topic_messages(topic: str, n_questions: int) -> list:
        """Returns a list of messages that ask the assistant to provide a list of questions for a topic."""
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
                'content': f'Give me a list of {n_questions} very short and interesting questions related to the topic "{topic}".'
            },
        ]
        return messages
    @classmethod
    def get_possible_output_choices(cls, processed_message_info: str) -> list:
        """Returns a list of possible output choices for a given processed message info."""
        messages = [
            {
                'role': 'system',
                'content': f"""You are a very useful teacher who will respond only using json. 
                Do not prefix your responses with ```json. 
                You will help me choose the best ways to represent information given the information type. 
                Use the following guide to help you choose in which ways the information can be best represented:
                {cls.output_guide}

                Respond with the following format:
                """ + r"""
                {possible_outputs: ["text", "timeline", "table", "speech", "list"]}
"""
            },
            {
                'role': 'user',
                'content': f"""The text between [[[ ]]] is a summary of a document. 
                Please tell me in wich ways I could best represent the information in the document. 
                Use the following guide to help you choose in which ways the information can be best represented (You can choose multiple ways):
                {cls.output_guide}
                [[[ {processed_message_info} ]]]"""
            },
        ]
        return messages
    